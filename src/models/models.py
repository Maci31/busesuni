from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    codigo: str
    facultad: str

class Register(BaseModel):
    codigo: str
    bus: str
    asiento: str
    paradero: str

class Ruta(BaseModel):
    ruta: str

class Facultad(BaseModel):
    nombre: str
    sigla: str

class Alumno(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    codigo: str
    facultad: str
    contrasena: str

class Paradero(BaseModel):
    nombre: str
    ruta: str