from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from model.model import Model
from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from config.config import ALLOWED_ORIGINS

app = FastAPI(
    title="Subsonic Festival API",
    version="1.0.0",
    description="API REST - Módulo de Autenticación"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mymodel = Model(factory=FirebaseDAOFactory())
sessions = {}

def verify_session(request: Request):
    """Verifica si el usuario tiene una sesión activa mediante cookie o header Authorization."""
    cookie = request.cookies.get("session")
    if cookie and cookie in sessions:
        return sessions[cookie]

    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        if token in sessions:
            return sessions[token]

    return None

@app.post("/register")
async def register_user(data: dict = Body(...)):
    """Endpoint TK-001-1: Registro de usuarios."""
    email = data.get("email")
    password = data.get("password")
    nombre = data.get("nombre")
    rol = data.get("rol", "cliente")

    if not email or not password or not nombre:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")

    uid = mymodel.create_usuario(email=email, password=password, nombre=nombre, rol=rol)
    if not uid:
        raise HTTPException(status_code=400, detail="No se pudo registrar el usuario")

    return JSONResponse(status_code=201, content={"message": "Usuario registrado", "uid": uid})

@app.post("/login")
async def login_user(data: dict = Body(...)):
    """Endpoint TK-001-1: Inicio de sesión de usuarios."""
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Credenciales requeridas")

    user_data = mymodel.login_usuario(email=email, password=password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    uid = user_data.get("uid")
    sessions[uid] = user_data

    response = JSONResponse(status_code=200, content={"message": "Login exitoso", "token": uid, "user": user_data})
    response.set_cookie(key="session", value=uid, httponly=True)
    return response

@app.post("/logout")
async def logout_user(request: Request):
    """Endpoint TK-001-1: Cierre de sesión."""
    user = verify_session(request)
    if user:
        uid = user.get("uid")
        sessions.pop(uid, None)

    response = JSONResponse(status_code=200, content={"message": "Sesión cerrada"})
    response.delete_cookie("session")
    return response