from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import List, Optional
from models import Suelo

class PlantaValid(BaseModel):
    nombre: str
    tipo: str
    tipo_suelo: Suelo

class PlantaActualizable(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    tipo_suelo: Optional[Suelo] = None

    @field_validator("nombre", "tipo")
    @classmethod
    def validar_no_vacio(cls, valor: Optional[str]) -> Optional[str]:
        if valor is not None:
            # Elimina espacios blancos en inicio y fin
            valor_limpio = valor.strip()

            # Si al limpiar queda vacío se lanza un error
            if not valor_limpio:
                raise ValueError("El campo no puede estrar vacío ni contener solo espacios en blanco.")

            return valor_limpio

        return valor

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