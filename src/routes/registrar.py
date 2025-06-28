from fastapi import APIRouter, Depends, HTTPException, Form, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from auth.service import AuthService
from database.crud import addRegister
from models.models import Register
from database.crud import getReservedSeats

registrar = APIRouter()
bearer_scheme = HTTPBearer()

def get_token_from_cookie(request: Request):
    token = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token no encontrado en las cookies")
    return token

@registrar.post("/register-asiento")
def register_asiento(bus: str = Form(...),asiento: str = Form(...), paradero: str = Form(...),token: str = Depends(get_token_from_cookie)):
    try:
        # token = get_token_from_cookie()
        # Verificar el token y obtener la información del usuario
        user_info = AuthService.verify_token(token)
        codigo = user_info.preferred_username  # Extraer el username del token

        # Crear el registro del asiento
        register_data = Register(
            codigo=codigo,
            bus=bus,
            asiento=asiento,
            paradero=paradero
        )
        result = addRegister(register_data)

        if result["status"] != "Registro agregado correctamente":
            raise HTTPException(status_code=400, detail=result["status"])

        return {"message": "Asiento registrado correctamente"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error al registrar el asiento: {str(e)}")

@registrar.get("/get-reserved-seats")
def get_reserved_seats(ruta: str = Query(...)):
    try:
        reserved_seats = getReservedSeats(ruta)
        return {"reserved_seats": reserved_seats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los asientos reservados: {str(e)}")



