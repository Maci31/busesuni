from datetime import datetime
from database.models import *
from database.db import SessionLocal
from models.models import *

# Agregar Alumno
def addUser(user: User):
    try:
        session = SessionLocal()
        # Verificar si ya existe un usuario con el mismo código
        existing_user = session.query(Alumnos).filter(Alumnos.codigo == user.codigo).first()
        if existing_user:
            session.close()
            return {"status": "Usuario con el mismo código ya existe"}

        # Agregar el nuevo usuario
        newuser = Alumnos(
            nombres=user.nombres,
            apellidos=user.apellidos,
            correo=user.correo,
            codigo=user.codigo,
            facultad=user.facultad,
            enable=True
        )
        session.add(newuser)
        session.commit()
        session.close()
        return {"status": "Usuario agregado correctamente"}
    except Exception as e:
        print(e)
        return {"status": str(e)}

# Listar Alumnos
def listUsers():
    try:
        session = SessionLocal()
        alumnos = session.query(Alumnos).filter(Alumnos.enable == True).all()
        for alumno in alumnos:
            print(f"Usuario: {alumno.nombres} {alumno.apellidos} codigo: {alumno.codigo}")
        session.close()
        return alumnos
    except Exception as e:
        print(e)
        return {"status": str(e)}

# Buscar un usuario en la tabla Alumnos
def searchUser(codigo: str):
    try:
        session = SessionLocal()
        alumno = session.query(Alumnos).filter(Alumnos.codigo == codigo, Alumnos.enable == True).first()
        session.close()
        if alumno:
            return {
                "nombres": alumno.nombres,
                "apellidos": alumno.apellidos,
                "correo": alumno.correo,
                "codigo": alumno.codigo,
                "facultad": alumno.facultad
            }
        else:
            return {"status": "Usuario no encontrado"}
    except Exception as e:
        print(e)
        return {"status": str(e)}

def deleteUser(user: User):
    try:
        session = SessionLocal()
        alumno = session.query(Alumnos).filter(Alumnos.codigo == user.codigo, Alumnos.enable == True).first()
        if alumno:
            alumno.enable = False
            session.commit()
            session.close()
            return {"status": "Usuario deshabilitado correctamente"}
        else:
            session.close()
            return {"status": "Usuario no encontrado o ya deshabilitado"}
    except Exception as e:
        print(e)
        return {"status": str(e)}

# Agregar registro
def addRegister(register: Register):
    try:
        session = SessionLocal()
        # Obtener la fecha de las 00:00 del día actual
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Verificar si el código ya tiene una reserva activa desde las 00:00 de hoy
        existing_reservation = session.query(Registros).filter(
            Registros.codigo == register.codigo,
            Registros.reservacion == True,
            Registros.timestamp >= today_start
        ).first()

        if existing_reservation:
            session.close()
            return {"status": "El usuario ya tiene una reserva activa desde las 00:00 de hoy"}

        # Verificar si el asiento ya está reservado desde las 00:00 de hoy
        existing_seat = session.query(Registros).filter(
            Registros.bus == register.bus,
            Registros.asiento == register.asiento,
            Registros.reservacion == True,
            Registros.timestamp >= today_start
        ).first()

        if existing_seat:
            session.close()
            return {"status": "El asiento ya está reservado desde las 00:00 de hoy"}

        # Agregar el nuevo registro
        new_register = Registros(
            fecha=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            timestamp=datetime.now(),
            codigo=register.codigo,
            bus=register.bus,
            paradero=register.paradero,
            asiento=register.asiento,
            reservacion=True
        )
        session.add(new_register)
        session.commit()
        session.close()
        return {"status": "Registro agregado correctamente"}
    except Exception as e:
        print(e)
        return {"status": str(e)}

def removeRegister(user: User):
    try:
        session = SessionLocal()
        # Obtener la fecha de las 00:00 del día actual
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Buscar la reserva activa del usuario desde las 00:00 de hoy
        existing_reservation = session.query(Registros).filter(
            Registros.codigo == user.codigo,
            Registros.reservacion == True,
            Registros.fecha >= today_start
        ).first()

        if not existing_reservation:
            session.close()
            return {"status": "No se encontró una reserva activa para el usuario desde las 00:00 de hoy"}

        # Eliminar la reserva
        session.delete(existing_reservation)
        session.commit()
        session.close()
        return {"status": "Reserva eliminada correctamente"}
    except Exception as e:
        print(e)
        return {"status": str(e)}

def getReservedSeats(ruta: str):
    try:
        session = SessionLocal()
        # Consulta a la base de datos para obtener los asientos reservados de la ruta
        reserved_seats = session.query(Registros.asiento).filter(Registros.bus == ruta).all()
        session.close()
        # Extraer los valores de los asientos de los resultados
        return [seat[0] for seat in reserved_seats]
    except Exception as e:
        print(f"Error al obtener los asientos reservados: {str(e)}")
        return []

