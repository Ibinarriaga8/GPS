"""
gps.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP02B
Integrantes:
    - Jorge Ibinarriaga
    - Miguel Angel Huamani 
    
"""
#LIBRERIAS
import grafo
import callejero
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import time
from callejero import cruces, direcciones, VELOCIDAD_CALLES_ESTANDAR, VELOCIDADES_CALLES

def distancia_entre_nodos(cruce1: callejero.Cruce, cruce2: callejero.Cruce):
    #Para encontrar la ruta más rápida
    return callejero.distancia(cruce1.coord_x, cruce1.coord_y, cruce2.coord_x, cruce2.coord_y)

def crear_grafo_distancia()->grafo.Grafo:
    """
    Grafo del callejero cuyo peso está determinado por la distancía física entre dos cruces
    """
    G = grafo.Grafo()
    V = list(callejero.procesar_cruces(cruces).values())
    [G.agregar_vertice(v) for v in V]
    calles_dict = callejero.procesar_calles(cruces)
    for calle in calles_dict.values():
        codigo_via = calle.codigo_via
        cruces_calle = calle.lista_cruces()
        i = 0
        if len(cruces_calle) > 1:
            while  i < len(cruces_calle)-1:
                nodo1, nodo2 = cruces_calle[i], cruces_calle[i+1]
                G.agregar_arista(nodo1, nodo2, weight = distancia_entre_nodos(nodo1, nodo2))
                i += 1
    return G

def crear_grafo_tiempo():
    """
    Grafo del callejero cuyo peso está determinado por las velocidades de las vías
    """
    G = grafo.Grafo()
    V = list(callejero.procesar_cruces(cruces).values())
    [G.agregar_vertice(v) for v in V]
    calles_dict = callejero.procesar_calles(cruces)
    for calle in calles_dict.values():
        codigo_via = calle.codigo_via
        cruces_calle = calle.lista_cruces()
        if len(direcciones[direcciones["Codigo de via"] == codigo_via]["Clase de la via"])>0:
            tipo_via = direcciones[direcciones["Codigo de via"] == codigo_via]["Clase de la via"].iloc[0].rstrip() 
            try:
                velocidad_maxima = VELOCIDADES_CALLES[tipo_via]
            except KeyError:
                velocidad_maxima = VELOCIDAD_CALLES_ESTANDAR
        else:
            velocidad_maxima = VELOCIDAD_CALLES_ESTANDAR 
        i = 0
        if len(cruces_calle) > 1:
            while  i < len(cruces_calle)-1:
                nodo1, nodo2 = cruces_calle[i], cruces_calle[i+1]
                G.agregar_arista(nodo1, nodo2, weight = velocidad_maxima)
                i += 1
    return G


def dibujar_grafo(G:grafo.Grafo):
    vertices = G.lista_vertices()
    posicion = dict()
    for vertice in vertices:
        posicion[vertice] = (vertice.coord_x, vertice.coord_y)
    G = G.convertir_a_NetworkX()
    nx.draw(G, pos=posicion, with_labels=False, node_color='blue', edge_color='black', node_size=0.1)
    plt.show()

def dibujar_ruta(camino, G):
    vertices = G.lista_vertices()
    G = G.convertir_a_NetworkX()
    posicion = dict()
    for vertice in vertices:
        posicion[vertice] = (vertice.coord_x, vertice.coord_y)
    nx.draw(G, pos=posicion, with_labels=False, node_color='blue', edge_color="gray", node_size=0.5)
    vertices_ruta = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
    ancho_aristas = [100 if (vertice1, vertice2) in camino or (vertice2, vertice1) in camino else 0.5 for vertice1, vertice2 in G.edges()]
    nx.draw_networkx_edges(G, edgelist=vertices_ruta, pos=posicion, edge_color='red', width=2)
    plt.show()


def cargar_direcciones(direcciones:pd.DataFrame)->dict:
    nombre_direcciones = direcciones["Clase de la via"].apply(lambda d: d.rstrip()) + direcciones['Particula de la via'].apply(lambda d: " " + d.rstrip()) + direcciones['Nombre de la via'].apply(lambda d: " "+d.rstrip()) + direcciones["Literal de numeracion"].apply(lambda d: " " + d.rstrip()) #keys
    coordenadas_direcciones = list(zip(direcciones["Coordenada X (Guia Urbana) cm"], direcciones["Coordenada Y (Guia Urbana) cm"])) #values
    diccionario_direcciones = dict(zip(nombre_direcciones, coordenadas_direcciones))
    return diccionario_direcciones


def obtener_informacion_direccion(cadena):
    match_calle = re.match(r"([^\d]+) NUM(\d+)", cadena)
    match_autovia = re.match(r"AUTOVIA\s+(A\-\d+)", cadena)

    if match_calle:
        nombre = match_calle.group(1).strip()
        numero = match_calle.group(2).lstrip("0")
        return {"tipo": "Calle", "nombre": nombre, "numero": numero}
    elif match_autovia:
        nombre = match_autovia.group(1).strip()
        return {"tipo": "Autovía", "nombre": nombre}


def encontrar_cruce_mas_cercano(direccion):
    """
    Encuentra el cruce más cercano a una dirección dada
    """
    diccionario_direcciones = cargar_direcciones(direcciones)
    coordenas_dir = diccionario_direcciones[direccion]
    cruces_dict = callejero.procesar_cruces(cruces)
    d_min = np.inf
    for cord_cruce in cruces_dict.keys():
        d = callejero.distancia(*coordenas_dir, *cord_cruce)
        if d <= d_min: 
            d_min = d
            cord_cruce_min = cord_cruce
    cruce_min = cruces_dict[cord_cruce_min]
    return cruce_min, d_min

def encontrar_ruta_minima(nodo_origen, nodo_destino, modo):
    """
    """
    if modo == "fastest":
        G = crear_grafo_tiempo()
    elif modo == "shortest":
        G = crear_grafo_distancia()
    camino = G.camino_minimo(nodo_origen, nodo_destino)
    return camino, G

def rotonda(nodo):
    return len(nodo.lista_calles()) > 3

def angulo_entre_vectores(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))

def determinar_sentido_giro(nodo1, nodo2, nodo3)->bool:
    """
    Devuelve True si el giro es a la derecha
    False si el giro es a la izquierda
    """
    vector_12 = (nodo2.coord_x - nodo1.coord_x, nodo2.coord_y - nodo1.coord_y)
    vector_13 = (nodo3.coord_x - nodo1.coord_x, nodo3.coord_y - nodo1.coord_y)
    return (angulo_entre_vectores(vector_12, vector_13) >= 0)
    
def obtener_calle_arista(nodo1, nodo2):
    calles_nodo1 = nodo1.calles
    calles_nodo2 = nodo2.calles
    calle_nodo = list(calles_nodo1.intersection(calles_nodo2))
    return calle_nodo[0] if calle_nodo != [] else ""


def determinar_sentido_giro(nodo1, nodo2, nodo3):
    return (nodo3.coord_x -nodo2.coord_x > 0)


def dirigir_ruta(direccion_origen, direccion_destino, modo = "fastest"):
    """
    Dado una dirección origen y una dirección destino de las direcciones, 
    da las indicaciones que sigue la ruta según el camino mínimo.
    """
    calle_origen = obtener_informacion_direccion(direccion_origen)["nombre"] 
    nodo_origen, d_or = encontrar_cruce_mas_cercano(direccion_origen)
    print("Cargando ruta...")
    nodo_destino, d_dest = encontrar_cruce_mas_cercano(direccion_destino)
    camino, G = encontrar_ruta_minima(nodo_origen, nodo_destino, modo)
    print(f"Continua por {calle_origen} {d_or/100} metros")
    i = 0
    for nodo in camino:
        time.sleep(0.3)
        if i < len(camino) - 1:
            calle_arista = obtener_calle_arista(camino[i], camino[i+1])
            distancia = distancia_entre_nodos(camino[i], camino[i+1])/100
            if rotonda(nodo):
                print(f"En la rotonda, sal por {calle_arista} y continua {distancia} metros por {calle_arista}")
            else:
                if obtener_calle_arista(camino[i-1], camino[i]) == obtener_calle_arista(camino[i], camino[i+1]):
                    print(f"Continua recto por {calle_arista} {distancia} metros ")
                else: # es un giro
                    nodo1 = camino[i-1]
                    nodo2 = camino[i]
                    nodo3 = camino[i+1]
                    if determinar_sentido_giro(nodo1, nodo2, nodo3):
                        print(f"Dirigite a la derecha y continua {distancia} metros por {calle_arista}")
                    else:
                        print(f"Dirigite a la izquierda y continua {distancia} metros por {calle_arista}")
            i+= 1


    calle_destino = obtener_informacion_direccion(direccion_destino)["nombre"] 
    print(f"Continua por {calle_destino} {d_dest/100} metros")
    print("Ha llegado a su destino")
    return camino, G

def dirigir_ruta_api(direccion_origen, direccion_destino, modo = "fastest"):
    """
    Dado una dirección origen y una dirección destino de las direcciones, 
    da las indicaciones que sigue la ruta según el camino mínimo.
    """
    calle_origen = obtener_informacion_direccion(direccion_origen)["nombre"] 
    nodo_origen, d_or = encontrar_cruce_mas_cercano(direccion_origen)
    print("Cargando ruta...")
    nodo_destino, d_dest = encontrar_cruce_mas_cercano(direccion_destino)
    camino, G = encontrar_ruta_minima(nodo_origen, nodo_destino, modo)
    print(f"Continua por {calle_origen} {d_or/100} metros")
    salida = []
    i = 0
    for nodo in camino:
        time.sleep(0.3)
        if i < len(camino) - 1:
            calle_arista = obtener_calle_arista(camino[i], camino[i+1])
            distancia = distancia_entre_nodos(camino[i], camino[i+1])/100
            if rotonda(nodo):
                salida.append(f"En la rotonda, sal por {calle_arista} y continua {distancia} metros por {calle_arista}")
            else:
                if obtener_calle_arista(camino[i-1], camino[i]) == obtener_calle_arista(camino[i], camino[i+1]):
                    salida.append(f"Continua recto por {calle_arista} {distancia} metros ")
                else: # es un giro
                    nodo1 = camino[i-1]
                    nodo2 = camino[i]
                    nodo3 = camino[i+1]
                    if determinar_sentido_giro(nodo1, nodo2, nodo3):
                        salida.append(f"Dirigite a la derecha y continua {distancia} metros por {calle_arista}")
                    else:
                        salida.append(f"Dirigite a la izquierda y continua {distancia} metros por {calle_arista}")
            i+= 1


    calle_destino = obtener_informacion_direccion(direccion_destino)["nombre"] 
    salida.append(f"Continua por {calle_destino} {d_dest/100} metros")
    salida.append("Ha llegado a su destino")
    return salida, G


