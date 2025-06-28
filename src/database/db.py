from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from config.readcrets import maincret, readenv

POSTGRES_USER = "buses"
POSTGRES_PASSWORD = "buses123"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 2345
POSTGRES_DB = "busesdb"


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(f"Database URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)
try:
    with engine.connect() as conn:
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
