import os
from pathlib import Path

# calcula la ruta base del backend para construir rutas absolutas de forma segura
BASE_DIR = Path(__file__).resolve().parent.parent

#  Configuración de FastAPI, se cargan desde variables de entorno con valores por defecto para desarrollo local
DEBUG = os.getenv("DEBUG", "True") == "True"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True") == "True"

#  Configuración CORS
# origen unico permitido para el frontend en produccion
ALLOWED_ORIGINS = [
    "http://subsonic-frontend-pi.dch9dvhue7chf8e0.polandcentral.azurecontainer.io:3000",
]

#  Rutas de archivos y credenciales
# ruta del archivo de credenciales que usa firebase admin para autenticar el backend
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "model", "dao", "firebase", "credentials.json")

# Sesiones 
# tiempo maximo de sesion en segundos para invalidacion por inactividad
SESSION_TIMEOUT = 3600  # 1 hora en segundos
# envia cookie no accesible desde javascript para mayor seguridad basica
SESSION_COOKIE_HTTPONLY = True
# en desarrollo se mantiene en false para permitir http local sin certificado
SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS

# Roles de usuario
# roles validos dentro de la aplicacion para control de permisos
AVAILABLE_ROLES = ["cliente", "proveedor", "gestor", "visitante"]

# Validaciones de entrada
# longitud minima y maxima de contrasena permitida en validaciones de entrada
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128

# Mensajes de error y exito
ERROR_MESSAGES = {
    "invalid_credentials": "Credenciales inválidas",
    "user_not_found": "Usuario no encontrado",
    "user_already_exists": "El usuario ya existe",
    "invalid_email": "Email inválido",
    "email_already_registered": "El email ya está registrado",
    "invalid_password": "La contraseña debe tener al menos 6 caracteres",
    "passwords_not_match": "Las contraseñas no coinciden",
    "unauthorized": "No autorizado",
    "forbidden": "Acceso denegado",
    "not_found": "No encontrado",
    "server_error": "Error interno del servidor",
}

SUCCESS_MESSAGES = {
    "login_success": "Inicio de sesión exitoso",
    "register_success": "Registro exitoso",
    "profile_updated": "Perfil actualizado",
    "order_created": "Pedido creado",
    "order_updated": "Pedido actualizado",
}

# Autenticación JWT local (TK-001-1)
JWT_SECRET = os.getenv("JWT_SECRET", "subsonic-dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 24))
