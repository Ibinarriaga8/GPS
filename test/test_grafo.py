"""
test_grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Descripción:
Script para verificación básica del funcionamiento de la librería grafo.py.

Las listas "vertices" y "aristas" describen un grafo (dirigido o no dirigido).
El script construye dicho grafo tomando pesos aleatorios en las aristas
usando la librería grafo.py.

Después realiza vairas operaciones básicas sobre el grafo y ejecuta sobre él:
    - Dijkstra
    - Búsqueda de un camino mínimo con Dijkstra
    - Prim
    - Kruskal
"""
import pytest
import grafo
import random

MIN_PESO_ARISTA=1
MAX_PESO_ARISTA=12

#Listas de vértices y aristas del grafo
dirigido=False
vertices=[1,2,3,4,5,6]
aristas=[(1,2),(1,3),(1,4),(1,5),(2,4),(3,4),(3,5),(5,6)]

@pytest.fixture
def grafo_instance():
    #Creación del grafo
    G=grafo.Grafo(dirigido)
    for v in vertices:
        G.agregar_vertice(v)
    for a in aristas:
        G.agregar_arista(a[0],a[1],None,random.randrange(MIN_PESO_ARISTA,MAX_PESO_ARISTA))
    return G

def test_grafo_creation(grafo_instance):
    G = grafo_instance
    for a in aristas:
        print(a[0],a[1],":",G.obtener_arista(a[0],a[1]))
        assert G.obtener_arista(a[0], a[1]) is not None

def test_grafo_operations(grafo_instance):
    G = grafo_instance
    #Eliminación de un vértice y una arista
    G.eliminar_vertice(6)
    G.eliminar_arista(1,5)

    #Grados de vértices y listas de adyacencia
    for v in vertices:
        print(v,":" , G.grado(v),G.grado_entrante(v),G.grado_saliente(v),G.lista_adyacencia(v))

    #Dijkstra y camino mínimo
    acm=G.dijkstra(1)
    print(acm)
    assert acm is not None

    camino=G.camino_minimo(1,5)
    print(camino)

    if(not dirigido):
        #Árbol abarcador mínimo
        aam=G.kruskal()
        print(aam)

        aam2=G.prim()
        print(aam2)