from fastapi import APIRouter, HTTPException, Form
from database.db import SessionLocal
from database.models import Alumnos
from models.models import Alumno
from auth.config import get_admin_config

alumnos = APIRouter()
keycloak_admin = get_admin_config()

@alumnos.post("/register")
def register_alumno(
    nombres: str = Form(...),
    apellidos: str = Form(...),
    correo: str = Form(...),
    codigo: str = Form(...),
    facultad: str = Form(...),
    contrasena: str = Form(...)
):
    session = SessionLocal()
    try:
        # Verificar si el usuario ya existe en la base de datos
        existing_user = session.query(Alumnos).filter(Alumnos.codigo == codigo).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El usuario ya existe en la base de datos")

        # Registrar el usuario en Keycloak
        crear_usuario = keycloak_admin.create_user({
            "username": codigo,
            "email": correo,
            "firstName": nombres,
            "lastName": apellidos,
            "enabled": True,
            "credentials": [{"type": "password", "value": contrasena, "temporary": False}]
        })

        print(f"Crear usuario: {crear_usuario}")

        # Agregar el usuario a la base de datos
        nuevo_alumno = Alumnos(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            codigo=codigo,
            facultad=facultad,
            enable=True
        )
        session.add(nuevo_alumno)
        session.commit()
        return {"status": "Usuario registrado correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar el usuario: {str(e)}")
    finally:
        session.close()

@alumnos.get("/list")
def list_alumnos():
    session = SessionLocal()
    try:
        alumnos = session.query(Alumnos).filter(Alumnos.enable == True).all()
        if not alumnos:
            raise HTTPException(status_code=404, detail="No se encontraron alumnos")
        return {"alumnos": [{"nombres": a.nombres, "apellidos": a.apellidos, "codigo": a.codigo, "facultad": a.facultad} for a in alumnos]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar alumnos: {str(e)}")
    finally:
        session.close()
