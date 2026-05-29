from dataclasses import dataclass
from datetime import datetime
from fastapi import FastAPI
from enum import Enum
from typing import Mapping, Any

# Conexion con la db
import sqlalchemy as db
import os


# Variables de entorno para evitar el hardcode
host = os.environ['DB_HOST']
pwd = os.environ['DB_PASSWORD']
usuario  = os.environ['DB_USER']

# Conexion con la db
engine = db.create_engine(f"postgresql://{usuario}:{pwd}@{host}:5433/cultibotdb")

# Inicializacion del metadata object
meta = db.MetaData()
meta.reflect(bind=engine)

# Tablas
PLANTAS = meta.tables['plantas']
METRICAS = meta.tables['metricas']

app = FastAPI()

class Suelo(Enum):
    ARENOSO = "arenoso"
    CALIZO = "calizo"
    TIERRA_NEGRA = "tierra negra"
    ARCILLOSO = "arcilloso"
    OTRO = "otro"

@dataclass(frozen=True)
class Planta:
    id: int
    nombre: str
    tipo: str
    tipo_suelo: Suelo

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Planta":
        """Construye una Planta a partir de una fila de la BD"""
        return cls(
            id=row["id_planta"],
            nombre=row["nombre"],
            tipo=row["tipo"],
            tipo_suelo=Suelo(row["tipo_suelo"])
        )

@dataclass(frozen=True)
class Nutriente:
    nitrogeno: float
    potasio: float
    fosforo: float

@dataclass(frozen=True)
class Metrica:
    id: int
    planta: Planta
    humedad_suelo: float
    temperatura_ambiente: float
    luminosidad: float
    nutrientes: Nutriente
    fecha: datetime

    @classmethod
    def from_joined_row(cls, row: Mapping[str, Any]) -> "Metrica":
        """Construye una Metrica y su Planta anidada a partir del JOIN"""
        return cls(
            id=row["id_metrica"],  # Asegúrate de que así se llame en tu BD
            humedad_suelo=float(row["humedad_suelo"]),
            temperatura_ambiente=float(row["temperatura_ambiente"]),
            luminosidad=float(row["luminosidad"]),
            fecha=row["fecha"],
            # Construimos el DTO Planta interno
            planta=Planta.from_row(row),
            # Construimos el DTO Nutriente interno
            nutrientes=Nutriente(
                nitrogeno=float(row["nitrogeno"]),
                potasio=float(row["potasio"]),
                fosforo=float(row["fosforo"])
            )
        )

@app.get("/")
def todas_plantas():
    query = db.select(PLANTAS).order_by(PLANTAS.c.id_planta.desc())
    with engine.connect() as conn:
        plantas = conn.execute(query).mappings().fetchall()
    plantas_list = [Planta.from_row(p) for p in plantas]
    return {"plantas":plantas_list}


@app.get("/metricas") # http://127.0.0.1:8000/metricas?id=1
def metricas(id: int = 0):
    query = (
        db.select(PLANTAS, METRICAS)
        .join(METRICAS, PLANTAS.c.id_planta == METRICAS.c.id_planta)
        .where(PLANTAS.c.id_planta == id)
        .order_by(METRICAS.c.fecha.desc())
    )
    with engine.connect() as conn:
        plantas = conn.execute(query).mappings().fetchall()
    
    if not plantas:
        return {"error": "Planta no encontrada"}, 404
    
    metricas_list = [Metrica.from_joined_row(p) for p in plantas]
    return {"metricas": metricas_list}

@app.get("/ultimaMetrica") # http://127.0.0.1:8000/ultimaMetrica?id=1
def ultima_metrica(id: int = 0):
    query = (
        db.select(PLANTAS, METRICAS)
        .join(METRICAS, PLANTAS.c.id_planta == METRICAS.c.id_planta)
        .where(PLANTAS.c.id_planta == id)
        .order_by(METRICAS.c.fecha.desc())
        .limit(1)
    )
    with engine.connect() as conn:
        planta = conn.execute(query).mappings().first()
    
    if not planta:
        return {"error": "Planta no encontrada"}, 404
    
    metrica_dto = Metrica.from_joined_row(planta)
    return {"metrica": metrica_dto}