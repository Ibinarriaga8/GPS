"""
test_grafo.py

Discreet Mathematics - IMAT
ICAI, Universidad Pontificia Comillas

Description:
Script for basic verification of the operation of the grafo.py library.

The "vertices" and "aristas" lists describe a graph (directed or undirected).
The script builds this graph taking random weights on the edges
using the grafo.py library.

Then it performs several basic operations on the graph and executes on it:
    - Dijkstra
    - Search for a minimum path with Dijkstra
    - Prim
    - Kruskal
"""
import pytest
import src.grafo as grafo
import random

MIN_PESO_ARISTA=1
MAX_PESO_ARISTA=12

#Vertices and edges lists of the graph
dirigido=False
vertices=[1,2,3,4,5,6]
aristas=[(1,2),(1,3),(1,4),(1,5),(2,4),(3,4),(3,5),(5,6)]

@pytest.fixture
def grafo_instance():
    #Graph creation
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
    #Deleting a vertex and an edge
    G.eliminar_vertice(6)
    G.eliminar_arista(1,5)

    #Vertex degrees and adjacency lists
    for v in vertices:
        print(v,":" , G.grado(v),G.grado_entrante(v),G.grado_saliente(v),G.lista_adyacencia(v))

    #Dijkstra and shortest path
    acm=G.dijkstra(1)
    print(acm)
    assert acm is not None

    camino=G.camino_minimo(1,5)
    print(camino)

    if(not dirigido):
        #Minimum spanning tree
        aam=G.kruskal()
        print(aam)

        aam2=G.prim()
        print(aam2)