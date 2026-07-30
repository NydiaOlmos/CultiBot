import sqlalchemy as db
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importa la base
from database import Base


class Suelo(Enum):
    ARENOSO = "Arenoso"
    CALIZO = "Calizo"
    TIERRA_NEGRA = "Tierra negra"
    ARCILLOSO = "Arcilloso"
    OTRO = "Otro"

class Planta(Base):
    __tablename__ = "plantas"

    id_planta: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(50))
    tipo: Mapped[str] = mapped_column(db.String(50))
    tipo_suelo: Mapped[Suelo] = mapped_column(db.Enum(Suelo, native_enum=False))

    metricas: Mapped[List["Metrica"]] = relationship(back_populates="planta", cascade="all, delete-orphan")

    def __repr__(self):
        return f"""Planta(
        id={self.id_planta!r}, 
        nombre={self.nombre!r}, 
        tipo={self.tipo!r}, 
        tipo_suelo={self.tipo_suelo!r}
        )"""

class Metrica(Base):
    __tablename__ = "metricas"

    id_metrica: Mapped[int] = mapped_column(primary_key=True)
    id_planta: Mapped[int] = mapped_column(db.ForeignKey("plantas.id_planta"))
    humedad_suelo: Mapped[Optional[float]]
    temperatura_ambiente: Mapped[Optional[float]]
    luminosidad: Mapped[Optional[float]]
    nitrogeno: Mapped[Optional[float]]
    potasio: Mapped[Optional[float]]
    fosforo: Mapped[Optional[float]]
    fecha: Mapped[datetime] = mapped_column(db.DateTime)

    planta: Mapped["Planta"] = relationship(back_populates="metricas")

    def __repr__(self):
        return f"""Metrica(
        id_metrica={self.id_metrica!r},
        id_planta={self.id_planta!r},
        humedad_suelo={self.humedad_suelo!r},
        temperatura_ambiente={self.temperatura_ambiente!r},
        luminosidad={self.luminosidad!r},
        nitrogeno={self.nitrogeno!r},
        potasio={self.potasio!r},
        fosforo={self.fosforo!r},
        fecha={self.fecha!r}
        )"""
