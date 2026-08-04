# Para correr el back
# fastapi dev

# Manejo de las peticiones a la api
from fastapi import FastAPI, Depends, HTTPException

# Manejo de la base de datos
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, contains_eager
from datetime import datetime

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

# Funciones de validación
def valida_existencia_planta(session: Session, id: int = 0):
    planta = session.get(Planta, id)

    # Verificamos que exista la planta
    if not planta:
        raise HTTPException(status_code=404, detail="Planta no encontrada")

    return planta

def valida_existencia_metrica_planta(session: Session, id: int = 0, id_metrica: int = 0):
    # Válida la planta
    valida_existencia_planta(session, id)
    
    # Verifica que exista la métrica
    metrica = session.get(Metrica, id_metrica)
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")

    # Verifica que exista la métrica en la planta
    if id != metrica.id_planta:
        raise HTTPException(status_code=400, detail="La planta no tiene esa métrica")
    
    return metrica

# ********************* CREATE ****************************
# Añade los datos de prueba al dataset
# http://127.0.0.1:8000/prueba
@app.post("/prueba", status_code=204)
def datos_prueba(session: Session = Depends(get_session)):
    if not carga_datos_prueba(session):
        raise HTTPException(status_code=404, detail="Ha surgido un problema con la carga de datos")

# Agrega una nueva planta
# http://127.0.0.1:8000/
@app.post("/", status_code=201, response_model=PlantaSchema)
def crear_planta(planta_data: PlantaCreable, session: Session = Depends(get_session)):
    # Convertir el esquema de Pydantic a SQLAlchemy
    nueva_planta = Planta(
        nombre = planta_data.nombre,
        tipo = planta_data.tipo,
        tipo_suelo = planta_data.tipo_suelo
    )

    # Añade la planta a la db
    session.add(nueva_planta)
    session.commit()
    session.refresh(nueva_planta) # Actualiza la planta para obtener el id

    return nueva_planta

# Agregar una nueva métrica
# http://127.0.0.1:8000/metricas?id=1
@app.post("/metricas", status_code=201, response_model=PlantaConMetricasResponse)
def crear_metrica(metrica_data: MetricaCreable, id:int = 0, session: Session = Depends(get_session)):
    # Verificamos que exista la planta
    planta = valida_existencia_planta(session, id)
    
    # Añade la nueva métrica
    nueva_metrica = Metrica(
        id_planta = id,
        humedad_suelo = metrica_data.humedad_suelo,
        temperatura_ambiente = metrica_data.temperatura_ambiente,
        luminosidad = metrica_data.luminosidad,
        nitrogeno = metrica_data.nitrogeno,
        potasio = metrica_data.potasio,
        fosforo = metrica_data.fosforo,
        fecha = datetime.now()
    )

    session.add(nueva_metrica)
    session.commit()
    session.refresh(planta) # Refresca la planta con la nueva métrica

    # Retornamos la planta con la métrica recien agregada
    query = (
        select(Planta)
        .join(Planta.metricas)
        .where(Planta.id_planta == id)
        .order_by(Metrica.fecha.desc())
        .limit(1)
        .options(contains_eager(Planta.metricas)) # Utiliza los registros ya filtados para poblar la lista de métricas
    )

    planta_con_metrica = session.scalar(query)

    return planta_con_metrica

# ********************* READ ****************************
# Recupera todas las plantas para la vista inicial
# http://127.0.0.1:8000/
@app.get("/", status_code=200, response_model=list[PlantaSchema])
def todas_plantas(session: Session = Depends(get_session)):
    query = select(Planta).order_by(Planta.id_planta.desc())
    plantas = session.scalars(query).all()

    if not plantas:
        raise HTTPException(status_code=204, detail="No hay plantas registradas")
    
    return plantas

# Extrae todas las métricas de una planta para graficarlas
# http://127.0.0.1:8000/metricas?id=1
@app.get("/metricas", status_code=200, response_model=PlantaConMetricasResponse) 
def metricas(id: int = 0, session: Session = Depends(get_session)):
    # Verifica que la planta exista
    valida_existencia_planta(session, id)
    
    query = (
        select(Planta)
        .join(Planta.metricas)
        .where(Planta.id_planta == id)
        .options(selectinload(Planta.metricas))
    ) # El selectinload es lo que realiza la carga de la lista de métricas
    planta = session.scalar(query)
    
    if not planta:
        raise HTTPException(status_code=204, detail="La planta no tiene métricas")
    
    return planta

# Recupera la última métrica para mostrarlas en las cards
# http://127.0.0.1:8000/ultimaMetrica?id=1
@app.get("/ultimaMetrica", status_code=200, response_model=PlantaConMetricasResponse)
def ultima_metrica(id: int = 0, session: Session = Depends(get_session)):
    # Verifica que la planta exista
    valida_existencia_planta(session, id)
    
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
        raise HTTPException(status_code=204, detail="La planta no tiene métricas")
    
    return planta

# ********************* UPDATE ****************************
# Actualiza una planta
# http://127.0.0.1:8000/?id=1
@app.put("/", status_code=200, response_model=PlantaSchema)
def actualiza_planta(planta_data: PlantaActualizable, id: int = 0, session: Session = Depends(get_session)):
    # Válida que la planta exista
    planta = valida_existencia_planta(session, id)

    # Convierte el esquema en diccionario únicamente con los campos rellenados
    datos_dict = planta_data.model_dump(exclude_unset=True, exclude_none=True)

    # Asigna dinámicamente los valores actualizados al objeto planta
    for clave, valor in datos_dict.items():
        setattr(planta, clave, valor)

    # Guarda los datos actualizados en la db
    session.commit()
    session.refresh(planta)

    return planta

# Actualiza una métrica
# http://127.0.0.1:8000/metricas?id=1&id_metrica=1
@app.put("/metricas", status_code=200, response_model=PlantaConMetricasResponse)
def actualiza_metrica(metrica_data: MetricaActualizable,id: int = 0, id_metrica: int = 0, session: Session = Depends(get_session)):
    # Verificamos que la planta y la métrica existan
    metrica = valida_existencia_metrica_planta(session, id, id_metrica)
    
    # Convertimos el equema en diccionario
    datos_dict = metrica_data.model_dump(exclude_unset=True) # Permitimos los null y none

    # Asigna dinámicamente los valores actualizados al objeto metrica
    for clave, valor in datos_dict.items():
        setattr(metrica, clave, valor)

    # Guarda los datos actualizados en la db
    session.commit()
    session.refresh(metrica)

    query = (
        select(Planta)
        .join(Planta.metricas)
        .where(Planta.id_planta == id and Metrica.id_metrica == id_metrica)
        .limit(1)
        .options(contains_eager(Planta.metricas)) # Utiliza los registros ya filtados para poblar la lista de métricas
    )

    planta = session.scalar(query)

    return planta

# ********************* DELETE ****************************
# Elimina una planta
# http://127.0.0.1:8000/?id=1
@app.delete("/", status_code=204)
def elimina_planta(id: int = 0, session: Session = Depends(get_session)):
    # Verificamos que la planta existe
    planta = valida_existencia_planta(session, id)
    
    session.delete(planta)
    session.commit()

# Elimina una métrica
# http://127.0.0.1:8000/metricas?id=1&id_metrica=1
@app.delete("/metricas", status_code=204)
def elimina_metrica(id: int = 0, id_metrica: int = 0, session: Session = Depends(get_session)):
    # Verificamos que la planta exista
    metrica = valida_existencia_metrica_planta(session, id, id_metrica)
    
    # Elimina la métrica
    session.delete(metrica)
    session.commit()