from fastapi import APIRouter, HTTPException
from database.db import SessionLocal
from database.models import Paraderos, Registros
from models.models import Paradero
from sqlalchemy import func

paraderos = APIRouter()

@paraderos.post("/addparadero")
def addparadero(paradero: Paradero):
    try:
        session = SessionLocal()
        # Verificar si ya existe un paradero con el mismo nombre
        existing_paradero = session.query(Paraderos).filter(Paraderos.nombre == paradero.nombre).first()
        if existing_paradero:
            session.close()
            raise HTTPException(status_code=400, detail="El paradero ya existe")

        # Crear un nuevo paradero
        nuevo_paradero = Paraderos(
            nombre=paradero.nombre,
            ruta=paradero.ruta
        )
        session.add(nuevo_paradero)
        session.commit()
        session.close()
        return {"status": "Paradero agregado correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@paraderos.delete("/deleteparadero")
def deleteparadero(paradero: Paradero):
    try:
        session = SessionLocal()
        # Buscar el paradero por su nombre
        existing_paradero = session.query(Paraderos).filter(Paraderos.nombre == paradero.nombre).first()
        if not existing_paradero:
            session.close()
            raise HTTPException(status_code=404, detail="El paradero no existe")

        # Eliminar el paradero
        session.delete(existing_paradero)
        session.commit()
        session.close()
        return {"status": "Paradero eliminado correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@paraderos.get("/getparaderos")
def getparaderos():
    try:
        session = SessionLocal()
        # Obtener todos los paraderos
        paraderos = session.query(Paraderos).all()
        session.close()
        if not paraderos:
            raise HTTPException(status_code=404, detail="No se encontraron paraderos")

        # Formatear los paraderos en una lista de diccionarios
        paraderos_list = [{"id": paradero.id, "nombre": paradero.nombre, "ruta": paradero.ruta} for paradero in paraderos]
        return {"status": "Paraderos obtenidos correctamente", "paraderos": paraderos_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@paraderos.put("/updateparadero")
def updateparadero(nombre_actual: str, nuevo_paradero: Paradero):
     try:
         session = SessionLocal()
         # Buscar el paradero actual por su nombre
         existing_paradero = session.query(Paraderos).filter(Paraderos.nombre == nombre_actual).first()
         if not existing_paradero:
             session.close()
             raise HTTPException(status_code=404, detail="El paradero no existe")

         # Actualizar el paradero
         existing_paradero.nombre = nuevo_paradero.nombre
         existing_paradero.ruta = nuevo_paradero.ruta
         session.commit()
         session.close()
         return {"status": "Paradero actualizado correctamente"}
     except Exception as e:
         session.rollback()
         raise HTTPException(status_code=500, detail=str(e))


@paraderos.get("/getasientos")
def get_asientos_por_ruta(ruta: str):
    try:
        session = SessionLocal()
        # Consultar el número de asientos por paradero en la ruta especificada
        resultados = (
            session.query(Registros.paradero, func.count(Registros.asiento).label("asientos"))
            .filter(Registros.bus == ruta)
            .group_by(Registros.paradero)
            .all()
        )
        session.close()
        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron paraderos para la ruta especificada")

        # Formatear los resultados en una lista de diccionarios
        asientos_por_paradero = [{"nombre": resultado[0], "asientos": resultado[1]} for resultado in resultados]
        return {"status": "Asientos obtenidos correctamente", "asientos_por_paradero": asientos_por_paradero}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@paraderos.get("/getasientos_completos_por_paradero")
def get_asientos_completos_por_paradero(ruta: str):
    try:
        session = SessionLocal()
        # Consultar la lista completa de paraderos y la cantidad de asientos por paradero en la ruta especificada
        resultados = (
            session.query(Paraderos.nombre, func.coalesce(func.count(Registros.asiento), 0).label("asientos"))
            .outerjoin(Registros, Paraderos.nombre == Registros.paradero)
            .filter(Paraderos.ruta == ruta)
            .group_by(Paraderos.nombre)
            .all()
        )
        session.close()
        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron paraderos para la ruta especificada")

        # Formatear los resultados en una lista de diccionarios
        paraderos_con_asientos = [{"paradero": resultado[0], "asientos": resultado[1]} for resultado in resultados]
        return {"status": "Datos obtenidos correctamente", "paraderos_con_asientos": paraderos_con_asientos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@paraderos.get("/getparaderos_por_ruta")
def get_paraderos_por_ruta(ruta: str):
    try:
        session = SessionLocal()
        # Consultar los paraderos de la ruta especificada
        paraderos = session.query(Paraderos).filter(Paraderos.ruta == ruta).all()
        session.close()
        if not paraderos:
            raise HTTPException(status_code=404, detail="No se encontraron paraderos para la ruta especificada")

        # Formatear los resultados en una lista de diccionarios
        paraderos_list = [{"id": paradero.id, "nombre": paradero.nombre} for paradero in paraderos]
        return {"status": "Paraderos obtenidos correctamente", "paraderos": paraderos_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
