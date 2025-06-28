from database.init_db import init_db
from fastapi import FastAPI, HTTPException, Request, Response, status, Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.models import *
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from auth.models import TokenResponse, UserInfo
from auth.controller import AuthController
from routes import rutas, facultades, alumnos, registrar, paraderos
from routes.alumnos import register_alumno
import uvicorn 

app = FastAPI()
bearer_scheme = HTTPBearer()
templates = Jinja2Templates(directory="templates")

init_db()


def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no encontrado en las cookies")
    return token


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    token_response = AuthController.login(username, password)
    if not token_response:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )
    response = RedirectResponse(url="/asientos", status_code=303)
    response.set_cookie(key="Authorization", value=f"{token_response.access_token}", httponly=True)
    return response



@app.post("/v1/adduser", tags=["Users"])
def adduser(user: User):
    try:
        return {"message": f"Usuario {user.nombres} agregado con éxito"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/asientos", response_class=HTMLResponse)
def asientos(request: Request):
    # Aquí puedes cargar los datos de los buses desde la base de datos
    buses = [
        {"id": 1, "name": "Bus 1"},
        {"id": 2, "name": "Bus 2"},
        {"id": 3, "name": "Bus 3"}
    ]
    return templates.TemplateResponse("asientos.html", {"request": request, "buses": buses})

@app.get("/registro", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/protected", response_model=UserInfo)
def protected(token: str = Depends(get_token_from_cookie)):
    return AuthController.protected_endpoint(token)



app.include_router(rutas.rutas, tags=["Rutas"])#, dependencies=[Depends(get_token_from_cookie)])
app.include_router(facultades.facultades, tags=["Facultad"])
app.include_router(alumnos.alumnos, tags=["Alumnos"])
app.include_router(registrar.registrar, tags=["Registrar"])
app.include_router(paraderos.paraderos, tags=["Paraderos"])


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000)









