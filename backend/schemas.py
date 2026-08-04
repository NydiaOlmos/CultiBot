from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from models import Suelo

class PlantaValid(BaseModel):
    nombre: str
    tipo: str
    tipo_suelo: Suelo

class MetricaValid(BaseModel):
    humedad_suelo: Optional[float]
    temperatura_ambiente: Optional[float]
    luminosidad: Optional[float]
    nitrogeno: Optional[float]
    potasio: Optional[float]
    fosforo: Optional[float]

class PlantaSchema(BaseModel):
    id_planta: int
    nombre: str
    tipo: str
    tipo_suelo: Suelo

    model_config = ConfigDict(from_attributes=True)

class MetricaSchema(BaseModel):
    id_metrica: int
    humedad_suelo: Optional[float]
    temperatura_ambiente: Optional[float]
    luminosidad: Optional[float]
    nitrogeno: Optional[float]
    potasio: Optional[float]
    fosforo: Optional[float]
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)

class PlantaConMetricasResponse(BaseModel):
    id_planta: int
    nombre: str
    tipo: str
    tipo_suelo: Suelo

    metricas: List[MetricaSchema] = []

    model_config = ConfigDict(from_attributes=True)