"""Endpoints de autenticación local con JWT (TK-001-1)."""
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError

from security.password import hash_password, is_strong_password, verify_password
from security.tokens import create_access_token, decode_access_token, revoke_token

router = APIRouter(prefix="/api/auth/local", tags=["auth-local"])

# Almacén local de demostración. En producción se usa Firebase/Firestore.
LOCAL_USERS = {}


def _seed_demo_users():
    demo = {
        "cliente.demo@subsonicfest.com": ("Cliente123!", "cliente", "Cliente Demo"),
        "proveedor.demo@subsonicfest.com": ("Proveedor123!", "proveedor", "Proveedor Demo"),
        "gestor.demo@subsonicfest.com": ("Gestor123!", "gestor", "Gestor Demo"),
        "admin.demo@subsonicfest.com": ("Admin123!", "admin", "Admin Demo"),
    }
    for email, (password, role, name) in demo.items():
        LOCAL_USERS[email] = {
            "uid": "local-" + email.split("@")[0],
            "email": email,
            "name": name,
            "role": role,
            "password_hash": hash_password(password),
            "suspended": False,
            "created_at": datetime.now().isoformat(),
        }


_seed_demo_users()


def _public_user(user: dict) -> dict:
    return {k: v for k, v in user.items() if k != "password_hash"}


def _bearer_token(request: Request) -> str:
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:].strip()
    return ""


@router.post("/register")
async def local_register(data: dict = Body(...)):
    """Registro local con validación de contraseña segura."""
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()

    if not email or not password or not name:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
    if not is_strong_password(password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos 8 caracteres, una mayúscula y un número",
        )
    if email in LOCAL_USERS:
        raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado")

    role = (data.get("role") or "cliente").strip().lower()
    if role not in {"cliente", "proveedor", "gestor", "admin"}:
        role = "cliente"

    user = {
        "uid": "local-" + email.replace("@", "-"),
        "email": email,
        "name": name,
        "role": role,
        "password_hash": hash_password(password),
        "suspended": False,
        "created_at": datetime.now().isoformat(),
    }
    LOCAL_USERS[email] = user
    token = create_access_token(user["uid"], user["role"], user["email"])

    return JSONResponse(
        status_code=201,
        content={"status": "success", "message": "Usuario registrado", "token": token, "user": _public_user(user)},
    )


@router.post("/login")
async def local_login(data: dict = Body(...)):
    """Inicio de sesión local. Devuelve JWT de 24 horas."""
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = LOCAL_USERS.get(email)

    # Mensaje genérico para no revelar si falla el correo o la contraseña.
    if not user or not verify_password(password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if user.get("suspended"):
        raise HTTPException(status_code=403, detail="Tu cuenta se encuentra suspendida")

    token = create_access_token(user["uid"], user["role"], user["email"])
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Inicio de sesión exitoso", "token": token, "user": _public_user(user)},
    )


@router.get("/me")
async def local_me(request: Request):
    """Devuelve el perfil asociado al JWT."""
    token = _bearer_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="No autorizado")
    try:
        claims = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = LOCAL_USERS.get(claims.get("email", ""))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return JSONResponse(status_code=200, content={"status": "success", "user": _public_user(user)})


@router.post("/logout")
async def local_logout(request: Request):
    """Revoca el token actual."""
    token = _bearer_token(request)
    revoke_token(token)
    return JSONResponse(status_code=200, content={"status": "success", "message": "Sesión cerrada"})
