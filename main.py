import inquirer
from difflib import SequenceMatcher, get_close_matches
import gps
from callejero import direcciones
nombre_direcciones = gps.cargar_direcciones(direcciones).keys()

def seleccionar_calle(message):
    direccion = input(message)
    coincidencias = get_close_matches(direccion.upper(), nombre_direcciones)

    nombre_direcciones_ordenadas = sorted(nombre_direcciones, key=lambda x: coincidencias.index(x) if x in coincidencias else float('inf'))
    preguntas = [inquirer.List('calle', message, choices = list(nombre_direcciones_ordenadas)[:3])]

    respuestas = inquirer.prompt(preguntas)
    calle_seleccionada = respuestas['calle']
    print(f"Has seleccionado: {calle_seleccionada}")
    return calle_seleccionada

def elegir_modo()->str:
    modo = input("Pulse S si desea encontrar la ruta más corta ó F si desea encontrar la ruta más rápida: ").upper()
    if modo == "F":
        modo = "fastest"
    elif modo == "S":
        modo = "shortest"
    else:
        modo = "fastest" #modo por defecto
    return modo

if __name__ == "__main__":
    print(".....Bienvenido a GPS IMAT.....")
    origen = seleccionar_calle(message = "Seleccione la dirección del origen: ")
    destino = seleccionar_calle(message= "Seleccione la dirección del destino: ")
    modo = elegir_modo()
    camino, G = gps.dirigir_ruta(origen, destino, modo)
    gps.dibujar_ruta(camino, G)
