"""
grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Group: GP2B
Members:
    - Jorge Ibinarriaga
    - Miguel Angel Huamani

Description:
Library for creating and analyzing directed and undirected graphs.
"""

from typing import List,Tuple,Dict
import networkx as nx
import sys

import heapq #Library for creating priority queues

INFTY = sys.float_info.max # "Infinite" distance between nodes of a graph


def es_hasheable(v):
    try:
        hash(v)
    except TypeError:
        raise TypeError("El objeto no es hashable")


class Grafo():
    """
    Class that stores a directed or undirected graph and provides tools
    for its analysis.
    """

    def __init__(self,dirigido:bool=False):
        """ Creates a directed or undirected graph.
        
        Args:
            dirigido (bool): Flag indicating whether the graph is directed (true) or not (false).

        Returns:
            Graph or directed graph (as indicated by the flag)
            initialized without vertices or edges.
        """

        # Flag indicating whether the graph is directed or not.
        self.dirigido=dirigido

        """
        Dictionary that stores the adjacency list of the graph.
        adyacencia[u]:  dictionary whose keys are the adjacency of u
        adyacencia[u][v]:   Content of the edge (u,v), i.e., pair (a,w) formed
                            by the object stored in the edge "a" (object) and its weight "w" (float).
        """
        self.adyacencia:Dict[object,Dict[object,Tuple[object,float]]]={}

    #### Operaciones básicas del TAD ####
    def es_dirigido(self)->bool:
        """ Indicates whether the graph is directed or not
        
        Args: None
        Returns: True if the graph is directed, False if not.
        Raises: None
        """
        if self.es_dirigido:
            return True
        else:
            return False
    
    def agregar_vertice(self,v:object)->None:
        """ Adds the vertex v to the graph.
        
        Args:
            v (object): vertex to be added. Must be "hashable".
        Returns: None
        Raises:
            TypeError: If the object is not "hashable".
        """

        es_hasheable(v)

        if v not in self.adyacencia:
            self.adyacencia[v] = {}


    def agregar_arista(self,s:object,t:object,data:object=None,weight:float=1)->None:
        """ If the objects s and t are vertices of the graph, adds
        an edge to the graph that goes from vertex s to vertex t
        and associates the data "data" and the weight weight.
        Otherwise, it does nothing.
        
        Args:
            s (object): source vertex.
            t (object): target vertex.
            data (object, optional): edge data. Defaults to None.
            weight (float, optional): edge weight. Defaults to 1.
        Returns: None
        Raises:
            TypeError: If s or t are not "hashable".
        """

        es_hasheable(s)
        es_hasheable(t)

        if s and t in self.adyacencia:
            self.adyacencia[s][t] = (data,weight)
            if not self.dirigido and s != t:
                self.adyacencia[t][s] = (data, weight)
    
    def eliminar_vertice(self,v:object)->None:
        """ If the object v is a vertex of the graph, it is removed.
        If not, it does nothing.
        
        Args:
            v (object): vertex to be removed.
        Returns: None
        Raises:
            TypeError: If v is not "hashable".
        """

        es_hasheable(v)

        if v in self.adyacencia:
            del self.adyacencia[v]

        if self.dirigido:
            for vertice in self.adyacencia:
                for adyacente in list(self.adyacencia[vertice]):
                    if adyacente[0] == v:
                        del self.adyacencia[vertice][adyacente]

        else:
            for vertice in self.adyacencia:
                if v in self.adyacencia[vertice]:
                    del self.adyacencia[vertice][v]

    def eliminar_arista(self,s:object,t:object)->None:
        """ If the objects s and t are vertices of the graph and there is
        an edge from u to v, it is removed.
        If not, it does nothing.
        
        Args:
            s: source vertex of the edge.
            t: target vertex of the edge.
        Returns: None
        Raises:
            TypeError: If s or t are not "hashable".
        """
    
        es_hasheable(s)
        es_hasheable(t)

        if s in self.adyacencia and t in self.adyacencia[s]:
            del self.adyacencia[s][t]


    def obtener_arista(self,s:object,t:object)->Tuple[object,float]:
        """ If the objects s and t are vertices of the graph and there is
        an edge from u to v, returns its data and weight in a tuple.
        If not, returns None
        
        Args:
            s: source vertex of the edge.
            t: target vertex of the edge.
        Returns:
            Tuple[object,float]: A tuple (a,w) with the data "a" of the edge (s,t) and its weight
                "w" if the edge exists.
            None: If the edge (s,t) does not exist in the graph.
        Raises:
            TypeError: If s or t are not "hashable".
        """

        es_hasheable(s)
        es_hasheable(t)

        if s in self.adyacencia and t in self.adyacencia[s]:
            return self.adyacencia[s][t]
        

    def lista_vertices(self)->List[object]:
        """ Returns a list with the vertices of the graph.
        
        Args: None
        Returns:
            List[object]: A list [v1,v2,...,vn] of the vertices of the graph.
        Raises: None
        """

        lista_vertices = []

        for v in self.adyacencia.keys():
            lista_vertices.append(v)

        return lista_vertices
    
    def lista_aristas(self)->List[object]:
        """
        Returns a list with all the edges of the graph and their respective weights
        """
        aristas = []
        for origen, adyacentes in self.adyacencia.items():
            for destino, (_, peso) in adyacentes.items():
                aristas.append((origen, destino, peso))
        return aristas

    def lista_adyacencia(self,u:object)->List[object]:
        """ If the object u is a vertex of the graph, returns
        its adjacency list, i.e., a list [v1,...,vn] with the vertices
        such that (u,v1), (u,v2),..., (u,vn) are edges of the graph.
        If not, returns None.
        
        Args: u vertex of the graph
        Returns:
            List[object]: A list [v1,v2,...,vn] of the vertices of the graph
                adjacent to u if u is a vertex of the graph
            None: if u is not a vertex of the graph
        Raises:
            TypeError: If u is not "hashable".
        """
        es_hasheable(u)

        lista_adyacencia = []

        if u in self.adyacencia:
            for v in self.adyacencia[u].keys():
                lista_adyacencia.append(v)

            return lista_adyacencia


    #### Grados de vértices ####
    def grado_saliente(self,v:object)-> int:
        """ If the object v is a vertex of the graph, returns
        its outgoing degree, i.e., the number of edges that start from v.
        If not, returns None.
        
        Args:
            v (object): vertex of the graph
        Returns:
            int: The outgoing degree of u if the vertex exists
            None: If the vertex does not exist.
        Raises:
            TypeError: If u is not "hashable".
        """
        es_hasheable(v)

        if v in self.adyacencia:
            return len(self.adyacencia[v]) 



    def grado_entrante(self,v:object)->int:
        """ If the object v is a vertex of the graph, returns
        its incoming degree, i.e., the number of edges that arrive at v.
        If not, returns None.
        
        Args:
            v (object): vertex of the graph
        Returns:
            int: The incoming degree of u if the vertex exists
            None: If the vertex does not exist.
        Raises:
            TypeError: If v is not "hashable".
        """
        es_hasheable(v)

        if v in self.adyacencia:
            grado_entrante = 0

            for vertice in self.adyacencia:
                if v in self.adyacencia[vertice]:
                    grado_entrante += 1
            
            return grado_entrante


    def grado(self,v:object)->int:
        """ If the object v is a vertex of the graph, returns
        its degree if the graph is not directed and its outgoing degree if
        it is directed.
        If it does not belong to the graph, returns None.
        
        Args:
            v (object): vertex of the graph
        Returns:
            int: The degree or outgoing degree of u as appropriate
                if the vertex exists
            None: If the vertex does not exist.
        Raises:
            TypeError: If v is not "hashable".
        """
        
        es_hasheable(v)

        if v in self.adyacencia:
            return len(self.adyacencia[v]) 
            

    #### Algoritmos ####
    def dijkstra(self,origen:object)-> Dict[object,object]:
        """ Calculates a Minimum Path Tree for the graph starting
        from the vertex "origen" using Dijkstra's algorithm. It only calculates
        the tree of the connected component that contains "origen".
        
        Args:
            origen (object): vertex of the graph of origin
        Returns:
            Dict[object,object]: Returns a dictionary that indicates, for each reachable vertex
                from "origen", which vertex is its parent in the minimum path tree.
        Raises:
            TypeError: If origen is not "hashable".
        Example:
            If G.dijksra(1)={2:1, 3:2, 4:1} then 1 is parent of 2 and 4 and 2 is parent of 3.
            In particular, a minimum path from 1 to 3 would be 1->2->3.
        """
        
        es_hasheable(origen)

        distancias = {vertice: float('inf') for vertice in self.adyacencia}
        padres = {vertice: None for vertice in self.adyacencia}
        distancias[origen] = 0

        vertices_restantes = set(self.adyacencia.keys())

        while vertices_restantes:
            vertice_actual = min(vertices_restantes, key=lambda v: distancias[v])
            vertices_restantes.remove(vertice_actual)

            for vecino, peso in self.adyacencia[vertice_actual].items():
                nueva_distancia = distancias[vertice_actual] + peso[1]
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = vertice_actual

        return padres
    

    def camino_minimo(self,origen:object,destino:object)->List[object]:
        """ Calculates the minimum path from the origin vertex to the
        destination vertex using Dijkstra's algorithm.
        
        Args:
            origen (object): vertex of the graph of origin
            destino (object): vertex of the graph of destination
        Returns:
            List[object]: Returns a list with the vertices of the graph through which it passes
                the shortest path between the origin and the destination. The first element of
                the list is origin and the last destination.
        Example:
            If G.camino_minimo(1,4)=[1,5,2,4] then the shortest path in G between 1 and 4 is 1->5->2->4.
        Raises:
            TypeError: If origen or destino are not "hashable".
        """

        es_hasheable(origen)
        es_hasheable(destino)

        padres = self.dijkstra(origen)

       # Reconstruir el camino desde el destino hasta el origen
        camino = [destino]
        while camino[-1] != origen:
            camino.append(padres[camino[-1]])

        # Invertir el camino para que vaya desde el origen hasta el destino
        return camino[::-1]


    def prim(self)-> Dict[object,object]:
        """ Calculates a Minimum Spanning Tree for the graph
        using Prim's algorithm.
        
        Args: None
        Returns:
            Dict[object,object]: Returns a dictionary that indicates, for each vertex of the
                graph, which vertex is its parent in the minimum spanning tree.
        Raises: None
        Example:
            If G.prim()={2:1, 3:2, 4:1} then in a minimum spanning tree we have that:
                1 is parent of 2 and 4
                2 is parent of 3
        """
        # Conjunto para almacenar los vértices ya visitados
        visitados = set()

        # Diccionario para almacenar los vértices y sus padres en el árbol abarcador mínimo
        padres = {list(self.adyacencia.keys())[0]: None}

        while len(visitados) < len(self.adyacencia):
            # Obtener el vértice con la arista más corta hacia un vértice no visitado
            min_arista = float('inf')
            min_vertice = None

            for vertice in padres:
                for vecino, peso_arista in self.adyacencia[vertice].items():
                    if vecino not in visitados and peso_arista[1] < min_arista:
                        min_arista = peso_arista[1]
                        min_vertice = vecino

            if min_vertice is not None:
                padres[min_vertice] = vertice
                visitados.add(min_vertice)

        return padres
                    

    def kruskal(self)-> List[Tuple[object,object]]:
        """ Calculates a Minimum Spanning Tree for the graph
        using Kruskal's algorithm.
        
        Args: None
        Returns:
            List[Tuple[object,object]]: Returns a list [(s1,t1),(s2,t2),...,(sn,tn)]
                of the pairs of vertices of the graph that form the edges
                of the minimum spanning tree.
        Raises: None
        Example:
            In the previous example in which G.kruskal()={2:1, 3:2, 4:1} we could have, for example,
            G.prim=[(1,2),(1,4),(3,2)]
        """
        
        # Obtener todas las aristas del grafo con sus respectivos pesos
        aristas = self.lista_aristas()

        # Ordenar las aristas por peso
        aristas.sort(key=lambda x: x[2])

        # Estructuras de datos para Kruskal
        arbol = []
        padres = {v: v for v in self.adyacencia}

        def buscar(v):
            while v != padres[v]:
                v = padres[v]
            return v

        def unir(v1, v2):
            raiz_v1 = buscar(v1)
            raiz_v2 = buscar(v2)
            padres[raiz_v1] = raiz_v2

        # Algoritmo de Kruskal
        for s, t, peso in aristas:
            if buscar(s) != buscar(t):
                arbol.append((s, t))
                unir(s, t)

        return arbol
    


    #### NetworkX ####
    def convertir_a_NetworkX(self)-> nx.Graph:
        """ Builds a Networkx graph or digraph as appropriate
        from the data of the current graph.
        
        Args: None
        Returns:
            networkx.Graph: Graph object from NetworkX if the graph is undirected.
            networkx.DiGraph: DiGraph object if the graph is directed.
            In both cases, the vertices and edges are those contained in the given graph.
        Raises: None
        """
        if self.dirigido:
            grafo = nx.DiGraph()
        else:
            grafo = nx.Graph()

        # Agregar vértices al grafo de NetworkX
        grafo.add_nodes_from(self.adyacencia.keys())

        # Agregar aristas al grafo de NetworkX
        for u, vecinos in self.adyacencia.items():
            for v, (_, peso) in vecinos.items():
                grafo.add_edge(u, v, weight=peso)  # Puedes especificar un atributo 'weight' si es necesario

        return grafo
    
def es_hasheable(v):
    """
    Check if the object is hashable
    """
    try:
        hash(v)
    except TypeError:
        raise TypeError("The object is not hashable")
