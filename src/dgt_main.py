import pandas as pd
import re
def cruces_read():
    cruces = pd.read_csv("data/cruces.csv", encoding = "windows-1252", sep = ";")
    return cruces

def clean_names(cruces: pd.DataFrame):
    columnas = list(cruces)[1:10]
    columnas.remove("Codigo de via que cruza o enlaza")
    for columna in columnas:
        cruces[columna] = cruces[columna].apply(lambda via: via.rstrip())
    return cruces

def cruces_as_int(cruces: pd.DataFrame):
    columnas = ["Codigo de via tratado", "Codigo de via que cruza o enlaza", "Coordenada X (Guia Urbana) cm (cruce)", "Coordenada Y (Guia Urbana) cm (cruce)"]
    for columna in columnas:
        cruces[columna] = cruces[columna].apply(lambda num: int(num))
    return cruces

def direcciones_read():
    return pd.read_csv("data/direcciones.csv",encoding = "windows-1252", sep = ";")

def direcciones_as_int(direcciones: pd.DataFrame):
    columnas = ["Codigo de numero", "Codigo de via", "Coordenada X (Guia Urbana) cm", "Coordenada Y (Guia Urbana) cm"]
    for columna in columnas:
        # Tu patrón regex
        pattern = re.compile(r"(\d+)")
        direcciones[columna] = direcciones[columna].apply(lambda num: int(pattern.match(str(num)).group(1)))
    return direcciones

def literal_split(direcciones: pd.DataFrame):
    pattern = re.compile(r"([A-Z]+\.?)(\d+)([A-Z]*)")
    direcciones["Prefijo de numeracion"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[1])
    direcciones["Numero"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[2])
    direcciones["Sufijo de numeracion"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[3])
    return direcciones

def process_data(cruces: pd.DataFrame, direcciones: pd.DataFrame):
    #Procesar cruces
    cruces = cruces_as_int(clean_names(cruces))
    #Procesar direcciones
    direcciones = literal_split(direcciones_as_int(direcciones))
    return cruces, direcciones

