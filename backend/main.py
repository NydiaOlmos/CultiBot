# Para correr el back
# fastapi dev

# Manejo de las peticiones a la api
from fastapi import FastAPI

# Conexion con la db
import sqlalchemy as db
import os

# Manejo de la base de datos
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


# ------- Variables de entorno para evitar el hardcode -------
host = os.environ['DB_HOST']
pwd = os.environ['DB_PASSWORD']
usuario  = os.environ['DB_USER']


# ------- Creacion de la estructura de la base de datos -------
class Base(DeclarativeBase):
    pass

class Suelo(Enum):
    ARENOSO = "arenoso"
    CALIZO = "calizo"
    TIERRA_NEGRA = "tierra negra"
    ARCILLOSO = "arcilloso"
    OTRO = "otro"

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

# Conexion con la db
engine = db.create_engine(f"postgresql://{usuario}:{pwd}@{host}:5433/cultibotdb")

# Crea las tablas
Base.metadata.create_all(bind=engine)

# Creamos una session
session = Session(engine)

# ------- Manejo de las peticiones -------
app = FastAPI()

# Recupera todas las plantas para la vista inicial
@app.get("/")
def todas_plantas():
    query = db.select(Planta).order_by(Planta.id_planta.desc())
    plantas = session.execute(query)
    print(plantas)
    with engine.connect() as conn:
        plantas = conn.execute(query).mappings().fetchall()
    plantas_list = [Planta.from_row(p) for p in plantas]
    return {"plantas":plantas_list}

# Extrae todas las metricas de una planta para graficarlas
@app.get("/metricas") # http://127.0.0.1:8000/metricas?id=1
def metricas(id: int = 0):
    query = (
        db.select(Planta, Metrica)
        .join(Metrica, Planta.c.id_planta == Metrica.c.id_planta)
        .where(Planta.c.id_planta == id)
        .order_by(Metrica.c.fecha.desc())
    )
    with engine.connect() as conn:
        plantas = conn.execute(query).mappings().fetchall()
    
    if not plantas:
        return {"error": "Planta no encontrada"}, 404
    
    metricas_list = [Metrica.from_joined_row(p) for p in plantas]
    return {"metricas": metricas_list}

# Recupera la ultima metrica para mostrarlas en las cards
@app.get("/ultimaMetrica") # http://127.0.0.1:8000/ultimaMetrica?id=1
def ultima_metrica(id: int = 0):
    query = (
        db.select(Planta, Metrica)
        .join(Metrica, Planta.c.id_planta == Metrica.c.id_planta)
        .where(Planta.c.id_planta == id)
        .order_by(Metrica.c.fecha.desc())
        .limit(1)
    )
    with engine.connect() as conn:
        planta = conn.execute(query).mappings().first()
    
    if not planta:
        return {"error": "Planta no encontrada"}, 404
    
    metrica_dto = Metrica.from_joined_row(planta)
    return {"metrica": metrica_dto}