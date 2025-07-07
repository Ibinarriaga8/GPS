from fastapi import FastAPI
from pydantic import BaseModel
from gps import dirigir_ruta_api
from difflib import get_close_matches
from callejero import direcciones
import gps
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy load de direcciones
_nombre_direcciones = None

def get_nombre_direcciones():
    global _nombre_direcciones
    if _nombre_direcciones is None:
        logger.info("Cargando direcciones por primera vez...")
        _nombre_direcciones = gps.cargar_direcciones(direcciones).keys()
        logger.info(f"Se cargaron {_nombre_direcciones.__len__()} direcciones.")
    return _nombre_direcciones

app = FastAPI()

class RutaRequest(BaseModel):
    origen: str
    destino: str
    modo: str  # "distancia" o "tiempo"

class InputProcesser:
    @staticmethod
    def seleccionar_calle(direccion: str) -> str:
        direccion_upper = direccion.upper()
        nombre_direcciones = get_nombre_direcciones()
        coincidencias = get_close_matches(direccion_upper, nombre_direcciones, n=1, cutoff=0.6)
        
        if coincidencias:
            calle_seleccionada = coincidencias[0]
            logger.info(f"Seleccionado automáticamente: {calle_seleccionada} para entrada: {direccion}")
        else:
            calle_seleccionada = direccion_upper
            logger.warning(f"No se encontraron coincidencias claras para '{direccion}', usando tal cual.")
        
        return calle_seleccionada

    @staticmethod
    def elegir_modo(modo: str) -> str:
        if modo.upper() == "F":
            return "fastest"
        elif modo.upper() == "S":
            return "shortest"
        else:
            logger.warning(f"Modo '{modo}' no reconocido. Usando 'fastest' por defecto.")
            return "fastest"

@app.get("/")
def root():
    logger.info("API de rutas funcionando")
    return {"message": "API de rutas funcionando"}

@app.post("/ruta")
def obtener_ruta(req: RutaRequest):
    try:
        origen = InputProcesser.seleccionar_calle(req.origen)
        destino = InputProcesser.seleccionar_calle(req.destino)
        modo = InputProcesser.elegir_modo(req.modo)
        logger.info(f"Iniciando búsqueda de ruta: {origen} -> {destino}, modo {modo}")
        ruta, grafo = dirigir_ruta_api(origen, destino, modo)
        logger.info("Ruta obtenida")

        if not ruta:
            return {"error": "No se encontró ruta para esos parámetros"}

        return {"ruta": ruta}
    except Exception as e:
        logger.exception("Error al obtener la ruta")
        return {"error": str(e)}
