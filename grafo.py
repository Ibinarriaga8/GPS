"""
grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP2B
Integrantes:
    - Jorge Ibinarriaga
    - Miguel Angel Huamani

Descripción:
Librería para la creación y análisis de grafos dirigidos y no dirigidos.
"""

from typing import List,Tuple,Dict
import networkx as nx
import sys

import heapq #Librería para la creación de colas de prioridad

INFTY = sys.float_info.max #Distincia "infinita" entre nodos de un grafo


def es_hasheable(v):
    try:
        hash(v)
    except TypeError:
        raise TypeError("El objeto no es hashable")


class Grafo():
    """
    Clase que almacena un grafo dirigido o no dirigido y proporciona herramientas
    para su análisis.<
    """

    def __init__(self,dirigido:bool=False):
        """ Crea un grafo dirigido o no dirigido.
        
        Args:
            dirigido (bool): Flag que indica si el grafo es dirigido (verdadero) o no (falso).

        Returns:
            Grafo o grafo dirigido (según lo indicado por el flag)
            inicializado sin vértices ni aristas.
        """

        # Flag que indica si el grafo es dirigido o no.
        self.dirigido=dirigido

        """
        Diccionario que almacena la lista de adyacencia del grafo.
        adyacencia[u]:  diccionario cuyas claves son la adyacencia de u
        adyacencia[u][v]:   Contenido de la arista (u,v), es decir, par (a,w) formado
                            por el objeto almacenado en la arista "a" (object) y su peso "w" (float).
        """
        self.adyacencia:Dict[object,Dict[object,Tuple[object,float]]]={}

    #### Operaciones básicas del TAD ####
    def es_dirigido(self)->bool:
        """ Indica si el grafo es dirigido o no
        
        Args: None
        Returns: True si el grafo es dirigido, False si no.
        Raises: None
        """
        if self.es_dirigido:
            return True
        else:
            return False
    
    def agregar_vertice(self,v:object)->None:
        """ Agrega el vértice v al grafo.
        
        Args:
            v (object): vértice que se quiere agregar. Debe ser "hashable".
        Returns: None
        Raises:
            TypeError: Si el objeto no es "hashable".
        """

        es_hasheable(v)

        if v not in self.adyacencia:
            self.adyacencia[v] = {}


    def agregar_arista(self,s:object,t:object,data:object=None,weight:float=1)->None:
        """ Si los objetos s y t son vértices del grafo, agrega
        una arista al grafo que va desde el vértice s hasta el vértice t
        y le asocia los datos "data" y el peso weight.
        En caso contrario, no hace nada.
        
        Args:
            s (object): vértice de origen (source).
            t (object): vértice de destino (target).
            data (object, opcional): datos de la arista. Por defecto, None.
            weight (float, opcional): peso de la arista. Por defecto, 1.
        Returns: None
        Raises:
            TypeError: Si s o t no son "hashable".
        """

        es_hasheable(s)
        es_hasheable(t)

        if s and t in self.adyacencia:
            self.adyacencia[s][t] = (data,weight)
            if not self.dirigido and s != t:
                self.adyacencia[t][s] = (data, weight)
    
    def eliminar_vertice(self,v:object)->None:
        """ Si el objeto v es un vértice del grafo lo elimina.
        Si no, no hace nada.
        
        Args:
            v (object): vértice que se quiere eliminar.
        Returns: None
        Raises:
            TypeError: Si v no es "hashable".
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
        """ Si los objetos s y t son vértices del grafo y existe
        una arista de u a v la elimina.
        Si no, no hace nada.
        
        Args:
            s: vértice de origen de la arista (source).
            t: vértice de destino de la arista (target).
        Returns: None
        Raises:
            TypeError: Si s o t no son "hashable".
        """
    
        es_hasheable(s)
        es_hasheable(t)

        if s in self.adyacencia and t in self.adyacencia[s]:
            del self.adyacencia[s][t]


    def obtener_arista(self,s:object,t:object)->Tuple[object,float]:
        """ Si los objetos s y t son vértices del grafo y existe
        una arista de u a v, devuelve sus datos y su peso en una tupla.
        Si no, devuelve None
        
        Args:
            s: vértice de origen de la arista (source).
            t: vértice de destino de la arista (target).
        Returns:
            Tuple[object,float]: Una tupla (a,w) con los datos "a" de la arista (s,t) y su peso
                "w" si la arista existe.
            None: Si la arista (s,t) no existe en el grafo.
        Raises:
            TypeError: Si s o t no son "hashable".
        """

        es_hasheable(s)
        es_hasheable(t)

        if s in self.adyacencia and t in self.adyacencia[s]:
            return self.adyacencia[s][t]
        

    def lista_vertices(self)->List[object]:
        """ Devuelve una lista con los vértices del grafo.
        
        Args: None
        Returns:
            List[object]: Una lista [v1,v2,...,vn] de los vértices del grafo.
        Raises: None
        """

        lista_vertices = []

        for v in self.adyacencia.keys():
            lista_vertices.append(v)

        return lista_vertices
    
    def lista_aristas(self)->List[object]:
        """
        Devuelve una lista con todas las aristas del grafo y sus respectivos pesos
        """
        aristas = []
        for origen, adyacentes in self.adyacencia.items():
            for destino, (_, peso) in adyacentes.items():
                aristas.append((origen, destino, peso))
        return aristas

    def lista_adyacencia(self,u:object)->List[object]:
        """ Si el objeto u es un vértice del grafo, devuelve
        su lista de adyacencia, es decir, una lista [v1,...,vn] con los vértices
        tales que (u,v1), (u,v2),..., (u,vn) son aristas del grafo.
        Si no, devuelve None.
        
        Args: u vértice del grafo
        Returns:
            List[object]: Una lista [v1,v2,...,vn] de los vértices del grafo
                adyacentes a u si u es un vértice del grafo
            None: si u no es un vértice del grafo
        Raises:
            TypeError: Si u no es "hashable".
        """
        es_hasheable(u)

        lista_adyacencia = []

        if u in self.adyacencia:
            for v in self.adyacencia[u].keys():
                lista_adyacencia.append(v)

            return lista_adyacencia


    #### Grados de vértices ####
    def grado_saliente(self,v:object)-> int:
        """ Si el objeto v es un vértice del grafo, devuelve
        su grado saliente, es decir, el número de aristas que parten de v.
        Si no, devuelve None.
        
        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado saliente de u si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si u no es "hashable".
        """
        es_hasheable(v)

        if v in self.adyacencia:
            return len(self.adyacencia[v]) 



    def grado_entrante(self,v:object)->int:
        """ Si el objeto v es un vértice del grafo, devuelve
        su grado entrante, es decir, el número de aristas que llegan a v.
        Si no, devuelve None.
        
        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado entrante de u si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si v no es "hashable".
        """
        es_hasheable(v)

        if v in self.adyacencia:
            grado_entrante = 0

            for vertice in self.adyacencia:
                if v in self.adyacencia[vertice]:
                    grado_entrante += 1
            
            return grado_entrante


    def grado(self,v:object)->int:
        """ Si el objeto v es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.
        
        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado grado o grado saliente de u según corresponda
                si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si v no es "hashable".
        """
        
        es_hasheable(v)

        if v in self.adyacencia:
            return len(self.adyacencia[v]) 
            

    #### Algoritmos ####
    def dijkstra(self,origen:object)-> Dict[object,object]:
        """ Calcula un Árbol de Caminos Mínimos para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".
        
        Args:
            origen (object): vértice del grafo de origen
        Returns:
            Dict[object,object]: Devuelve un diccionario que indica, para cada vértice alcanzable
                desde "origen", qué vértice es su padre en el árbol de caminos mínimos.
        Raises:
            TypeError: Si origen no es "hashable".
        Example:
            Si G.dijksra(1)={2:1, 3:2, 4:1} entonces 1 es padre de 2 y de 4 y 2 es padre de 3.
            En particular, un camino mínimo desde 1 hasta 3 sería 1->2->3.
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
        """ Calcula el camino mínimo desde el vértice origen hasta el vértice
        destino utilizando el algoritmo de Dijkstra.
        
        Args:
            origen (object): vértice del grafo de origen
            destino (object): vértice del grafo de destino
        Returns:
            List[object]: Devuelve una lista con los vértices del grafo por los que pasa
                el camino más corto entre el origen y el destino. El primer elemento de
                la lista es origen y el último destino.
        Example:
            Si G.camino_minimo(1,4)=[1,5,2,4] entonces el camino más corto en G entre 1 y 4 es 1->5->2->4.
        Raises:
            TypeError: Si origen o destino no son "hashable".
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
        """ Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.
        
        Args: None
        Returns:
            Dict[object,object]: Devuelve un diccionario que indica, para cada vértice del
                grafo, qué vértice es su padre en el árbol abarcador mínimo.
        Raises: None
        Example:
            Si G.prim()={2:1, 3:2, 4:1} entonces en un árbol abarcador mínimo tenemos que:
                1 es padre de 2 y de 4
                2 es padre de 3
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
        """ Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.
        
        Args: None
        Returns:
            List[Tuple[object,object]]: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
                de los pares de vértices del grafo que forman las aristas
                del arbol abarcador mínimo.
        Raises: None
        Example:
            En el ejemplo anterior en que G.kruskal()={2:1, 3:2, 4:1} podríamos tener, por ejemplo,
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
        """ Construye un grafo o digrafo de Networkx según corresponda
        a partir de los datos del grafo actual.
        
        Args: None
        Returns:
            networkx.Graph: Objeto Graph de NetworkX si el grafo es no dirigido.
            networkx.DiGraph: Objeto DiGraph si el grafo es dirigido.
            En ambos casos, los vértices y las aristas son los contenidos en el grafo dado.
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
    
