"""
callejero.py

Discrete Mathematics - IMAT
ICAI, Universidad Pontificia Comillas

Group: GP02B
Members:
    - Jorge Ibinarriaga
    - Miguel Angel Huamani

Description:
Library with auxiliary tools and classes needed for the representation of a street map in a graph.

Complete this description according to the functionalities added by the group.
"""
import src.dgt_main as dgt_main
import pandas as pd
import math
import numpy as np
cruces = dgt_main.cruces_read()
direcciones = dgt_main.direcciones_read()
cruces, direcciones = dgt_main.process_data(cruces, direcciones)

# Constants with the maximum speeds established by the statement for each type of road.
VELOCIDADES_CALLES={"AUTOVIA":100,"AVENIDA":90,"CARRETERA":70,"CALLEJON":30,"CAMINO":30,"ESTACION DE METRO":20,"PASADIZO":20,"PLAZUELA":20,"COLONIA":20}
VELOCIDAD_CALLES_ESTANDAR=50

# ADDRESSES
def concatenar_vias(direcciones):
    """
    Concatenates the columns 'Street class', 'Street particle' and 'Street name' and unifies them in a single column
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

    # Complete this class with the data and methods needed to associate with each intersection

    def __init__(self,coord_x,coord_y, loc):
        self.coord_x=coord_x
        self.coord_y=coord_y
        self.calles = set()
        self.loc = loc # location
        # Complete the initialization of added data structures

    """The Cruce class is made "hashable" by implementing the
    __eq__ and __hash__ methods, making two objects of type Cruce considered equal when
    their coordinates match (i.e., C1==C2 if and only if C1 and C2 have the same coordinates),
    regardless of the other fields that may be stored in the objects.
    The __hash__ function is adapted accordingly 
    to only depend on the pair (coord_x, coord_y).
    """
    def agregar_calle(self, calle):
        self.calles.add(calle) 
    def lista_calles(self):
        return list(self.calles) # returns a list with all the streets at the intersection

    def __eq__(self,other) -> int:
        if type(other) is type(self):
            return ((self.coord_x==other.coord_x) and (self.coord_y==other.coord_y))
        else:
            return False
    
    def __hash__(self) -> int:
        return hash((self.coord_x,self.coord_y))
    
def distancia(x1:int,y1:int,x2:int,y2:int)->float:
    """
    Calculates the euclidean distance in R2.
    d: (x1,y1) x (x2,y2) -> R+
    """
    x,y = x2-x1, y2-y1
    return math.sqrt(x**2 + y**2)

    
def procesar_cruces(cruces: pd.DataFrame):
    global cruces_dict
    cruces = unificar_cruces(cruces)
    """
    From the intersections dataframe, intersections are stored in the Cruce class, 
    containing a list with all the streets that converge at that intersection.
    """
    df= cruces[["Coordenada X (Guia Urbana) cm (cruce)", "Coordenada Y (Guia Urbana) cm (cruce)", "Literal completo del vial tratado", "Literal completo del vial que cruza", "Longitud en S R  WGS84 (cruce)", "Latitud en S R  WGS84 (cruce)"]]
    cruces_dict = {}

    for index, row in df.iterrows():
        coord_x = row['Coordenada X (Guia Urbana) cm (cruce)']
        coord_y = row['Coordenada Y (Guia Urbana) cm (cruce)']
        loc = (row["Longitud en S R  WGS84 (cruce)"], row["Latitud en S R  WGS84 (cruce)"])
        coordendas_cruce = (coord_x, coord_y)
        if coordendas_cruce in cruces_dict.keys(): # the intersection already exists
            cruce = cruces_dict[coordendas_cruce]
        else:
            cruce = Cruce(coord_x, coord_y, loc) # create intersection
            cruces_dict[coordendas_cruce] = cruce
        cruce.agregar_calle(row['Literal completo del vial tratado'])
        cruce.agregar_calle(row["Literal completo del vial que cruza"])
    return cruces_dict
                                                           
class Calle:
    """
        Represents a street with its name, code, and intersections.

        Attributes:
            nombre (str): The name of the street.
            codigo_via (int): The unique code of the street.
            cruces (set): A set of intersections the street has.

        Methods:
            agregar_cruce(cruce): Adds an intersection to the street's set of intersections.
            lista_cruces(): Returns a list of all intersections the street has.
        """
    def __init__(self, nombre_calle, codigo_via):
        self.nombre = nombre_calle
        self.codigo_via = codigo_via
        self.cruces = set()
    def agregar_cruce(self, cruce):
        self.cruces.add(cruce)
    def lista_cruces(self):
        return list(self.cruces) # returns a list with all intersections on that street

def procesar_calles(cruces: pd.DataFrame)->dict:
    global cruces_dict
    """
    From the intersections dataframe, stores all streets with their respective intersections 
    in a dictionary with keys as the street name and values as the street object
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
        cruce = cruces_dict[coordendas_cruce] # get the intersection
        if not codigo_via in calles_dict.keys():
            calle = Calle(nombre_calle, codigo_via) # create street
            calle.agregar_cruce(cruce) # add intersection
            calles_dict[codigo_via] = calle
        else:
            calle = calles_dict[codigo_via]
        calle.agregar_cruce(cruce)
    return calles_dict



        




