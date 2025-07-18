from fastapi import FastAPI
from pydantic import BaseModel
from src.gps import dirigir_ruta_api
from difflib import get_close_matches
from src.callejero import direcciones
import src.gps as gps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy load of addresses
_nombre_direcciones = None

def get_nombre_direcciones():
    global _nombre_direcciones
    if _nombre_direcciones is None:
        logger.info("Loading addresses for the first time...")
        _nombre_direcciones = gps.cargar_direcciones(direcciones).keys()
        logger.info(f"Loaded {_nombre_direcciones.__len__()} addresses.")
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
            logger.info(f"Automatically selected: {calle_seleccionada} for input: {direccion}")
        else:
            calle_seleccionada = direccion_upper
            logger.warning(f"No clear matches found for '{direccion}', using it as is.")
        
        return calle_seleccionada

    @staticmethod
    def elegir_modo(modo: str) -> str:
        if modo.upper() == "F":
            return "fastest"
        elif modo.upper() == "S":
            return "shortest"
        else:
            logger.warning(f"Mode '{modo}' not recognized. Using 'fastest' by default.")
            return "fastest"

@app.get("/")
def root():
    logger.info("Route API running")
    return {"message": "Route API running"}

@app.post("/ruta")
def obtener_ruta(req: RutaRequest):
    try:
        origen = InputProcesser.seleccionar_calle(req.origen)
        destino = InputProcesser.seleccionar_calle(req.destino)
        modo = InputProcesser.elegir_modo(req.modo)
        logger.info(f"Starting route search: {origen} -> {destino}, mode {modo}")
        ruta, grafo = dirigir_ruta_api(origen, destino, modo)
        logger.info("Route obtained")

        if not ruta:
            return {"error": "No route found for those parameters"}

        return {"ruta": ruta}
    except Exception as e:
        logger.exception("Error getting the route")
        return {"error": str(e)}
