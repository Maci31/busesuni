from fastapi import APIRouter, HTTPException
from database.db import SessionLocal
from database.models import Facultades
from models.models import Facultad

facultades = APIRouter()

@facultades.post("/addfacultad")
def addfacultad(facultad: Facultad):
    try:
        session = SessionLocal()
        # Verificar si ya existe una facultad con el mismo nombre
        existing_facultad = session.query(Facultades).filter(Facultades.nombre == facultad.nombre).first()
        if existing_facultad:
            session.close()
            raise HTTPException(status_code=400, detail="La facultad ya existe")

        # Crear una nueva facultad
        nueva_facultad = Facultades(
            nombre=facultad.nombre,
            sigla=facultad.sigla
        )
        session.add(nueva_facultad)
        session.commit()
        session.close()
        return {"status": "Facultad agregada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@facultades.delete("/deletefacultad")
def deletefacultad(facultad: Facultad):
    try:
        session = SessionLocal()
        # Buscar la facultad por su nombre
        existing_facultad = session.query(Facultades).filter(Facultades.nombre == facultad.nombre).first()
        if not existing_facultad:
            session.close()
            raise HTTPException(status_code=404, detail="La facultad no existe")

        # Eliminar la facultad
        session.delete(existing_facultad)
        session.commit()
        session.close()
        return {"status": "Facultad eliminada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@facultades.get("/getfacultades")
def getfacultades():
    try:
        session = SessionLocal()
        # Obtener todas las facultades
        facultades = session.query(Facultades).all()
        session.close()
        if not facultades:
            raise HTTPException(status_code=404, detail="No se encontraron facultades")

        # Formatear las facultades en una lista de diccionarios
        facultades_list = [{"id": facultad.id, "nombre": facultad.nombre, "sigla": facultad.sigla} for facultad in facultades]
        return {"status": "Facultades obtenidas correctamente", "facultades": facultades_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@facultades.put("/updatefacultad")
def updatefacultad(nombre_actual: str, nueva_facultad: Facultad):
    try:
        session = SessionLocal()
        # Buscar la facultad actual por su nombre
        existing_facultad = session.query(Facultades).filter(Facultades.nombre == nombre_actual).first()
        if not existing_facultad:
            session.close()
            raise HTTPException(status_code=404, detail="La facultad no existe")

        # Actualizar la facultad
        existing_facultad.nombre = nueva_facultad.nombre
        existing_facultad.sigla = nueva_facultad.sigla
        session.commit()
        session.close()
        return {"status": "Facultad actualizada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@facultades.get("/getsiglas")
def get_siglas():
    try:
        session = SessionLocal()
        siglas = session.query(Facultades.sigla).all()
        session.close()
        if not siglas:
            raise HTTPException(status_code=404, detail="No se encontraron siglas")
        return {"siglas": [sigla[0] for sigla in siglas]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))