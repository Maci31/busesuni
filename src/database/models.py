from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.db import Base

class Rutas(Base):
    __tablename__ = 'Rutas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta = Column(String, nullable=False)

class Alumnos(Base):
    __tablename__ = 'Alumnos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    facultad = Column(String, nullable=False)
    enable = Column(Boolean, nullable=False)

class Facultades(Base):
    __tablename__ = 'Facultades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    sigla = Column(String, nullable=False)

class Registros(Base):
    __tablename__ = 'Registros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    codigo = Column(String, nullable=False)
    bus = Column(String, nullable=False)
    paradero = Column(String, nullable=False)
    asiento = Column(String, nullable=False)
    reservacion = Column(Boolean, nullable=False, default=False)

class Paraderos(Base):
    __tablename__ = 'Paraderos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    ruta = Column(String, nullable=False)