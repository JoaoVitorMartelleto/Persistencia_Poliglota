from geopy.distance import geodesic
from typing import Tuple, List, Dict

def calcular_distancia_km(a: Tuple[float,float], b: Tuple[float,float]) -> float:
    """Return geodesic distance in km between two (lat, lon) pairs."""
    return geodesic(a, b).km

def filtrar_locais_por_raio(locais: List[Dict], origem: Tuple[float,float], raio_km: float) -> List[Dict]:
    resultado = []
    for l in locais:
        coords = l.get("coordenadas")
        if coords and "coordinates" in coords:
            lon, lat = coords["coordinates"]
            dist = calcular_distancia_km(origem, (lat, lon))
            if dist <= raio_km:
                l["_dist_km"] = dist
                resultado.append(l)
    resultado.sort(key=lambda x: x["_dist_km"])
    return resultado