import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de servidor
DEBUG = os.getenv("DEBUG", "True") == "True"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True") == "True"

# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Rutas y Sesiones
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "model", "dao", "firebase", "credentials.json")
SESSION_TIMEOUT = 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False

AVAILABLE_ROLES = ["cliente", "proveedor", "gestor", "visitante"]