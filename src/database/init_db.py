from database.db import Base, engine
from database.models import Rutas, Alumnos, Facultades

# Crea las tablas si no existen
def init_db():
    Base.metadata.create_all(bind=engine)
