# Para correr el back
# fastapi dev

# Manejo de las peticiones a la api
from fastapi import FastAPI, Depends, HTTPException

# Manejo de la base de datos
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, contains_eager

# Importa la sesión y los modelos
from database import SessionLocal, engine
from models import *
from schemas import *

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
# http://127.0.0.1:8000/prueba
@app.post("/prueba", status_code=204)
def datos_prueba(session: Session = Depends(get_session)):
    if not carga_datos_prueba(session):
        raise HTTPException(status_code=404, detail="Ha surgido un problema con la carga de datos")

# Recupera todas las plantas para la vista inicial
# http://127.0.0.1:8000/
@app.get("/", status_code=200, response_model=list[PlantaSchema])
def todas_plantas(session: Session = Depends(get_session)):
    query = select(Planta).order_by(Planta.id_planta.desc())
    plantas = session.scalars(query).all()
    
    if not plantas:
        raise HTTPException(status_code=204, detail="No hay plantas registradas")
    
    return plantas

# Extrae todas las metricas de una planta para graficarlas
# http://127.0.0.1:8000/metricas?id=1
@app.get("/metricas", status_code=200, response_model=PlantaConMetricasResponse) 
def metricas(id: int = 0, session: Session = Depends(get_session)):
    query = (
        select(Planta, Metrica)
        .where(Planta.id_planta == id)
        .options(selectinload(Planta.metricas))
    ) # El selectinload es lo que realiza la carga de la lista de métricas
    planta = session.scalar(query)
    
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    
    return planta

# Recupera la ultima métrica para mostrarlas en las cards
# http://127.0.0.1:8000/ultimaMetrica?id=1
@app.get("/ultimaMetrica", status_code=200, response_model=PlantaConMetricasResponse)
def ultima_metrica(id: int = 0, session: Session = Depends(get_session)):
    query = (
        select(Planta)
        .join(Planta.metricas)
        .where(Planta.id_planta == id)
        .order_by(Metrica.fecha.desc())
        .limit(1)
        .options(contains_eager(Planta.metricas)) # Utiliza los registros ya filtados para poblar la lista de métricas
    )

    planta = session.scalar(query)
    
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    
    return planta