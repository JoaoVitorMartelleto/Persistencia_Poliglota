import os
from typing import List, Dict
from pymongo.collection import Collection
from geopy.distance import geodesic
from dotenv import load_dotenv
from pymongo import MongoClient, GEOSPHERE, errors

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "persistencia_poliglota"
COLLECTION_NAME = "locais"

def get_mongo_client(uri: str = MONGODB_URI) -> MongoClient:
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except errors.ServerSelectionTimeoutError as e:
        raise RuntimeError(f"Não foi possível conectar ao MongoDB em {uri!r}: {e}") from e

def get_locais_collection(client: MongoClient = None) -> Collection:
    if client is None:
        client = get_mongo_client()
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]
    try:
        coll.create_index([("coordenadas", GEOSPHERE)])
    except Exception:
        pass
    return coll

def inserir_local(nome_local: str, cidade: str, latitude: float, longitude: float, descricao: str = "") -> str:
    coll = get_locais_collection()
    doc = {
        "nome_local": nome_local,
        "cidade": cidade,
        "descricao": descricao,
        "coordenadas": {"type": "Point", "coordinates": [float(longitude), float(latitude)]}
    }
    res = coll.insert_one(doc)
    return str(res.inserted_id)

def buscar_locais_por_cidade(cidade: str, limite: int = 100) -> List[Dict]:
    coll = get_locais_collection()
    return list(coll.find({"cidade": cidade}).limit(limite))

def buscar_locais_proximos_geo(latitude: float, longitude: float, raio_km: float = 10, limite: int = 100) -> List[Dict]:
    """Use MongoDB $nearSphere (returns documents within raio_km)."""
    coll = get_locais_collection()
    raio_m = raio_km * 1000
    cursor = coll.find({
        "coordenadas": {
            "$nearSphere": {
                "$geometry": {"type": "Point", "coordinates": [float(longitude), float(latitude)]},
                "$maxDistance": raio_m
            }
        }
    }).limit(limite)
    return list(cursor)

def buscar_locais_proximos_fallback(latitude: float, longitude: float, raio_km: float = 10) -> List[Dict]:
    """Fallback: load all docs and compute distance with geopy (km)."""
    coll = get_locais_collection()
    all_docs = list(coll.find({}))
    origin = (float(latitude), float(longitude))
    result = []
    for d in all_docs:
        coords = d.get("coordenadas")
        if coords and "coordinates" in coords:
            lon, lat = coords["coordinates"]
            dist = geodesic(origin, (lat, lon)).km
            if dist <= raio_km:
                d["_dist_km"] = dist
                result.append(d)
    result.sort(key=lambda x: x["_dist_km"])
    return result
