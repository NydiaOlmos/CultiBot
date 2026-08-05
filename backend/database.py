# Conexión con la db
import sqlalchemy as db
import os

# Manejo de la base de datos
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ------- Variables de entorno para evitar el hardcode -------
host = os.environ['DB_HOST']
pwd = os.environ['DB_PASSWORD']
usuario  = os.environ['DB_USER']


# Conexión con la db
engine = db.create_engine(f"postgresql://{usuario}:{pwd}@{host}:5433/cultibotdb")

# Declaración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------- Creación de la estructura de la base de datos -------
class Base(DeclarativeBase):
    pass