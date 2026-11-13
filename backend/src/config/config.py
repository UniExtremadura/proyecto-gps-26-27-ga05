"""Configuración central del backend.

Todos los valores se pueden sobrescribir mediante variables de entorno o el
archivo ``backend/.env``. Los valores por defecto están pensados para el
entorno local de desarrollo (MongoDB en Docker y frontend en localhost).
"""
import os
from pathlib import Path

try:  # Carga .env si existe (python-dotenv es dependencia del proyecto).
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except Exception:  # pragma: no cover - la aplicación funciona sin .env
    pass

# Rutas base
SRC_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = SRC_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

# FastAPI
DEBUG = os.getenv("DEBUG", "True") == "True"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True") == "True"

# CORS: incluye los orígenes habituales del frontend local.
_default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", ",".join(_default_origins)).split(",")
    if origin.strip()
]
EXTRA_ALLOWED_ORIGINS = [
    origin.strip() for origin in os.getenv("EXTRA_ALLOWED_ORIGINS", "").split(",") if origin.strip()
]

# Base de datos local (contenedor MongoDB de docker-compose)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "subsonic")
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", 5000))
SEED_DEMO_DATA = os.getenv("SEED_DEMO_DATA", "True") == "True"

# Compatibilidad con el código heredado de Firebase
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "")

# Sesiones
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 3600))
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"

# Roles
AVAILABLE_ROLES = ["cliente", "proveedor", "gestor", "organizador", "admin", "visitante"]

# Validaciones
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128

ERROR_MESSAGES = {
    "invalid_credentials": "Credenciales incorrectas",
    "user_not_found": "Usuario no encontrado",
    "user_already_exists": "El usuario ya existe",
    "invalid_email": "Email inválido",
    "email_already_registered": "El correo electrónico ya está registrado",
    "invalid_password": "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número",
    "passwords_not_match": "Las contraseñas no coinciden",
    "unauthorized": "No autorizado",
    "forbidden": "Acceso denegado",
    "not_found": "No encontrado",
    "server_error": "Error interno del servidor",
    "suspended": "Tu cuenta se encuentra suspendida",
}

SUCCESS_MESSAGES = {
    "login_success": "Inicio de sesión exitoso",
    "register_success": "Usuario registrado",
    "profile_updated": "Perfil actualizado",
    "order_created": "Pedido creado",
}

# Autenticación JWT local
JWT_SECRET = os.getenv("JWT_SECRET", "subsonic-dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 24))

# SMTP simulado (Mailpit opcional)
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", "no-reply@subsonicfest.com")
