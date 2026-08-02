# Para correr el back
# fastapi dev

# Manejo de las peticiones a la api
from fastapi import FastAPI, Depends, HTTPException

# Manejo de la base de datos
from sqlalchemy import select
from sqlalchemy.orm import Session

# Importa la sesión y los modelos
from database import SessionLocal, engine
from models import *

# Datos de prueba
from datosPrueba import carga_datos_prueba


# Crea las tablas del models si es que aún no han sido creadas
Base.metadata.create_all(bind=engine)

# ------- Manejo de las peticiones -------
app = FastAPI()

# Generador de dependencia para abrir/cerrar la sesión en cada request
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Añade los datos de prueba al dataset
@app.post("/prueba", status_code=204)
def datos_prueba(session: Session = Depends(get_session)):
    if not carga_datos_prueba(session):
        raise HTTPException(status_code=404)

# Recupera todas las plantas para la vista inicial
@app.get("/", status_code=200)
def todas_plantas(session: Session = Depends(get_session)):
    query = select(Planta).order_by(Planta.id_planta.desc())
    plantas = session.scalars(query).all()
    return plantas

# Extrae todas las metricas de una planta para graficarlas
@app.get("/metricas", status_code=200) # http://127.0.0.1:8000/metricas?id=1
def metricas(id: int = 0, session: Session = Depends(get_session)):
    query = (
        select(Planta, Metrica)
        .join(Metrica, Planta.c.id_planta == Metrica.c.id_planta)
        .where(Planta.c.id_planta == id)
        .order_by(Metrica.c.fecha.desc())
    )
    plantas = session.scalars(query).all()
    
    if not plantas:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    
    # metricas_list = [Metrica.from_joined_row(p) for p in plantas]
    # return {"metricas": metricas_list}
    return plantas

# Recupera la ultima metrica para mostrarlas en las cards
@app.get("/ultimaMetrica", status_code=200) # http://127.0.0.1:8000/ultimaMetrica?id=1
def ultima_metrica(id: int = 0, session: Session = Depends(get_session)):
    query = (
        select(Planta, Metrica)
        .join(Metrica, Planta.c.id_planta == Metrica.c.id_planta)
        .where(Planta.c.id_planta == id)
        .order_by(Metrica.c.fecha.desc())
        .limit(1)
    )
    planta = session.scalar(query)
    
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    
    # metrica_dto = Metrica.from_joined_row(planta)
    # return {"metrica": metrica_dto}
    return planta