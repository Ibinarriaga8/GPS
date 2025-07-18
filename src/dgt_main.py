import pandas as pd
import re
def cruces_read():
    """Reads the cruces.csv file into a pandas DataFrame.

    Returns:
        pd.DataFrame: The cruces DataFrame.
    """
    cruces = pd.read_csv("data/cruces.csv", encoding = "windows-1252", sep = ";")
    return cruces

def clean_names(cruces: pd.DataFrame):
    """Cleans the names of the columns in the cruces DataFrame.

    Args:
        cruces (pd.DataFrame): The cruces DataFrame.

    Returns:
        pd.DataFrame: The cleaned cruces DataFrame.
    """
    columnas = list(cruces)[1:10]
    columnas.remove("Codigo de via que cruza o enlaza")
    for columna in columnas:
        cruces[columna] = cruces[columna].apply(lambda via: via.rstrip())
    return cruces

def cruces_as_int(cruces: pd.DataFrame):
    """Converts the specified columns in the cruces DataFrame to integers.

    Args:
        cruces (pd.DataFrame): The cruces DataFrame.

    Returns:
        pd.DataFrame: The cruces DataFrame with the specified columns converted to integers.
    """
    columnas = ["Codigo de via tratado", "Codigo de via que cruza o enlaza", "Coordenada X (Guia Urbana) cm (cruce)", "Coordenada Y (Guia Urbana) cm (cruce)"]
    for columna in columnas:
        cruces[columna] = cruces[columna].apply(lambda num: int(num))
    return cruces

def direcciones_read():
    """Reads the direcciones.csv file into a pandas DataFrame.

    Returns:
        pd.DataFrame: The direcciones DataFrame.
    """
    return pd.read_csv("data/direcciones.csv",encoding = "windows-1252", sep = ";")

def direcciones_as_int(direcciones: pd.DataFrame):
    """Converts the specified columns in the direcciones DataFrame to integers, extracting the first number found.

    Args:
        direcciones (pd.DataFrame): The direcciones DataFrame.

    Returns:
        pd.DataFrame: The direcciones DataFrame with the specified columns converted to integers.
    """
    columnas = ["Codigo de numero", "Codigo de via", "Coordenada X (Guia Urbana) cm", "Coordenada Y (Guia Urbana) cm"]
    for columna in columnas:
        # Your regex pattern
        pattern = re.compile(r"(\d+)")
        direcciones[columna] = direcciones[columna].apply(lambda num: int(pattern.match(str(num)).group(1)))
    return direcciones

def literal_split(direcciones: pd.DataFrame):
    """Splits the 'Literal de numeracion' column in the direcciones DataFrame into three new columns: 'Prefijo de numeracion', 'Numero', and 'Sufijo de numeracion'.

    Args:
        direcciones (pd.DataFrame): The direcciones DataFrame.

    Returns:
        pd.DataFrame: The direcciones DataFrame with the new columns.
    """
    pattern = re.compile(r"([A-Z]+\.?)(\d+)([A-Z]*)")
    direcciones["Prefijo de numeracion"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[1])
    direcciones["Numero"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[2])
    direcciones["Sufijo de numeracion"] = direcciones["Literal de numeracion"].apply(lambda direccion: pattern.match(direccion)[3])
    return direcciones

def process_data(cruces: pd.DataFrame, direcciones: pd.DataFrame):
    """Processes the cruces and direcciones DataFrames.

    Args:
        cruces (pd.DataFrame): The cruces DataFrame.
        direcciones (pd.DataFrame): The direcciones DataFrame.

    Returns:
        tuple: A tuple containing the processed cruces and direcciones DataFrames.
    """
    #Process cruces
    cruces = cruces_as_int(clean_names(cruces))
    #Process direcciones
    direcciones = literal_split(direcciones_as_int(direcciones))
    return cruces, direcciones
