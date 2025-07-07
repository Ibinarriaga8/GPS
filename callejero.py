"""
callejero.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP02B
Integrantes:
    - Jorge Ibinarriaga
    - Miguel Angel Huamani

Descripción:
Librería con herramientas y clases auxiliares necesarias para la representación de un callejero en un grafo.

Complétese esta descripción según las funcionalidades agregadas por el grupo.
"""
import dgt_main
import pandas as pd
import math
import numpy as np
cruces = dgt_main.cruces_read()
direcciones = dgt_main.direcciones_read()
cruces, direcciones = dgt_main.process_data(cruces, direcciones)
#Constantes con las velocidades máximas establecidas por el enunciado para cada tipo de vía.
VELOCIDADES_CALLES={"AUTOVIA":100,"AVENIDA":90,"CARRETERA":70,"CALLEJON":30,"CAMINO":30,"ESTACION DE METRO":20,"PASADIZO":20,"PLAZUELA":20,"COLONIA":20}
VELOCIDAD_CALLES_ESTANDAR=50

#DIRECCIONES
def concatenar_vias(direcciones):
    """
    Concatena las columnas 'Clase de via' 'Particula de  la via' y 'Nombre de la via' y las unifica en una misma columna
    """
    def concat_vias(row):
        return f"{row['Clase de la via'].rstrip()} {row['Particula de la via'].rstrip()} {row['Nombre de la vía'].rstrip()}"

    direcciones['Nombre completo de la vía'] = direcciones.apply(concat_vias, axis=1)
    return direcciones


def unificar_cruces(cruces, R=30*100):
    coordenadas = cruces[['Coordenada X (Guia Urbana) cm (cruce)', 'Coordenada Y (Guia Urbana) cm (cruce)']].to_numpy()

    for index, cruce in enumerate(coordenadas):
        distancias = np.sqrt(np.sum((coordenadas - cruce)**2, axis=1))
        cruces_cercanos = np.where(distancias < R)[0]

    if len(cruces_cercanos) > 1:
        x_media = coordenadas[cruces_cercanos, 0].mean()
        y_media = coordenadas[cruces_cercanos, 1].mean()

        indice_cruce_a_conservar = cruces_cercanos[0]
        indices_cruces_a_eliminar = cruces_cercanos[1:]

        cruces = cruces.drop(index=indices_cruces_a_eliminar)

        cruces.at[indice_cruce_a_conservar, 'Coordenada X (Guia Urbana) cm (cruce)'] = x_media
        cruces.at[indice_cruce_a_conservar, 'Coordenada Y (Guia Urbana) cm (cruce)'] = y_media

    return cruces


class Cruce:

    #Completar esta clase con los datos y métodos que se necesite asociar a cada cruce

    def __init__(self,coord_x,coord_y, loc):
        self.coord_x=coord_x
        self.coord_y=coord_y
        self.calles = set()
        self.loc = loc #localización
        #Completar la inicialización de las estructuras de datos agregadas

    """Se hace que la clase Cruce sea "hashable" mediante la implementación de los métodos
    __eq__ y __hash__, haciendo que dos objetos de tipo Cruce se consideren iguales cuando
    sus coordenadas coincidan (es decir, C1==C2 si y sólo si C1 y C2 tienen las mismas coordenadas),
    independientemente de los otros campos que puedan estar almacenados en los objetos.
    La función __hash__ se adapta en consecuencia 
    para que sólo dependa del par (coord_x, coord_y).
    """
    def agregar_calle(self, calle):
        self.calles.add(calle) 
    def lista_calles(self):
        return list(self.calles) #devuelve una lista con todas las calles del cruce

    def __eq__(self,other) -> int:
        if type(other) is type(self):
            return ((self.coord_x==other.coord_x) and (self.coord_y==other.coord_y))
        else:
            return False
    
    def __hash__(self) -> int:
        return hash((self.coord_x,self.coord_y))
    
def distancia(x1:int,y1:int,x2:int,y2:int)->float:
    """
    Calcula la distancia euclidea en R2.
    d: (x1,y1) x (x2,y2) -> R+
    """
    x,y = x2-x1, y2-y1
    return math.sqrt(x**2 + y**2)

    
def procesar_cruces(cruces: pd.DataFrame):
    global cruces_dict
    cruces = unificar_cruces(cruces)
    """
    A partir del dataframe de cruces, se almacenan los cruces en la clase Cruce, 
    conteniendo una lista con todas las calles que confluyen en ese cruce.
    """
    df= cruces[["Coordenada X (Guia Urbana) cm (cruce)", "Coordenada Y (Guia Urbana) cm (cruce)", "Literal completo del vial tratado", "Literal completo del vial que cruza", "Longitud en S R  WGS84 (cruce)", "Latitud en S R  WGS84 (cruce)"]]
    cruces_dict = {}

    for index, row in df.iterrows():
        coord_x = row['Coordenada X (Guia Urbana) cm (cruce)']
        coord_y = row['Coordenada Y (Guia Urbana) cm (cruce)']
        loc = (row["Longitud en S R  WGS84 (cruce)"], row["Latitud en S R  WGS84 (cruce)"])
        coordendas_cruce = (coord_x, coord_y)
        if coordendas_cruce in cruces_dict.keys(): #el cruce ya existe
            cruce = cruces_dict[coordendas_cruce]
        else:
            cruce = Cruce(coord_x, coord_y, loc) #crea cruce
            cruces_dict[coordendas_cruce] = cruce
        cruce.agregar_calle(row['Literal completo del vial tratado'])
        cruce.agregar_calle(row["Literal completo del vial que cruza"])
    return cruces_dict
                                                           
class Calle:
    def __init__(self, nombre_calle, codigo_via):
        self.nombre = nombre_calle
        self.codigo_via = codigo_via
        self.cruces = set()
    def agregar_cruce(self, cruce):
        self.cruces.add(cruce)
    def lista_cruces(self):
        return list(self.cruces) #devuelve una lista con todos los cruces en esa calle

def procesar_calles(cruces: pd.DataFrame)->dict:
    global cruces_dict
    """
    A partir del dataframe de cruces, almacena todas las calles con sus respectivos cruces 
    en un diccionario con claves el nombre de la calle y valores el objeto calle
    """
    procesar_cruces(cruces)
    list(cruces)
    df= cruces[["Coordenada X (Guia Urbana) cm (cruce)", "Coordenada Y (Guia Urbana) cm (cruce)", "Literal completo del vial tratado", "Literal completo del vial que cruza", "Longitud en S R  WGS84 (cruce)", "Latitud en S R  WGS84 (cruce)", "Codigo de via tratado"]]        
    calles_dict = dict()
    for index, row in df.iterrows():
        coord_x = row['Coordenada X (Guia Urbana) cm (cruce)']
        coord_y = row['Coordenada Y (Guia Urbana) cm (cruce)']
        nombre_calle = row['Literal completo del vial tratado']
        codigo_via = row["Codigo de via tratado"]
        coordendas_cruce = (coord_x, coord_y)
        cruce = cruces_dict[coordendas_cruce] #obtienes el cruce
        if not codigo_via in calles_dict.keys():
            calle = Calle(nombre_calle, codigo_via) #crear calle
            calle.agregar_cruce(cruce) #añadimos cruce
            calles_dict[codigo_via] = calle
        else:
            calle = calles_dict[codigo_via]
        calle.agregar_cruce(cruce)
    return calles_dict



        




