from fastapi import APIRouter, HTTPException
from database.db import SessionLocal
from database.models import Rutas
from models.models import Ruta
rutas = APIRouter()

@rutas.post("/addruta")
def addruta(ruta: Ruta):
    try:
        session = SessionLocal()
        # Verificar si ya existe una ruta con el mismo nombre
        existing_ruta = session.query(Rutas).filter(Rutas.ruta == ruta.ruta).first()
        if existing_ruta:
            session.close()
            raise HTTPException(status_code=400, detail="La ruta ya existe")

        # Crear una nueva ruta
        nueva_ruta = Rutas(
            ruta=ruta.ruta
        )
        session.add(nueva_ruta)
        session.commit()
        session.close()
        return {"status": "Ruta agregada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@rutas.delete("/deleteruta")
def deleteruta(ruta: Ruta):
    try:
        session = SessionLocal()
        # Buscar la ruta por su nombre
        existing_ruta = session.query(Rutas).filter(Rutas.ruta == ruta.ruta).first()
        if not existing_ruta:
            session.close()
            raise HTTPException(status_code=404, detail="La ruta no existe")

        # Eliminar la ruta
        session.delete(existing_ruta)
        session.commit()
        session.close()
        return {"status": "Ruta eliminada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@rutas.get("/getrutas")
def get_rutas():
    try:
        session = SessionLocal()
        rutas = session.query(Rutas.ruta).all()
        session.close()
        if not rutas:
            raise HTTPException(status_code=404, detail="No se encontraron rutas")
        return {"rutas": [ruta[0] for ruta in rutas]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rutas.put("/updateruta")
def updateruta(ruta_actual: str, nueva_ruta: Ruta):
    try:
        session = SessionLocal()
        # Buscar la ruta actual por su nombre
        existing_ruta = session.query(Rutas).filter(Rutas.ruta == ruta_actual).first()
        if not existing_ruta:
            session.close()
            raise HTTPException(status_code=404, detail="La ruta no existe")

        # Actualizar la ruta
        existing_ruta.ruta = nueva_ruta.ruta
        session.commit()
        session.close()
        return {"status": "Ruta actualizada correctamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))