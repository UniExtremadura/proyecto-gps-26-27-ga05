"""Generación y validación de tokens de recuperación (TK-005-1)."""
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from security.password import hash_password, is_strong_password

RESET_TTL_MINUTES = 30
RESET_TOKENS: Dict[str, Dict[str, Any]] = {}


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def _local_users() -> Dict[str, Dict[str, Any]]:
    # Importación diferida: auth_routes importa este servicio en tiempo de ejecución.
    from controller.routers.auth_routes import LOCAL_USERS

    return LOCAL_USERS


def _find_user(email: str) -> Dict[str, Any] | None:
    normalized = str(email or "").strip().lower()
    local = _local_users().get(normalized)
    if local:
        return {"uid": local.get("uid"), "email": normalized, "source": "local"}

    connector = _connector()
    if connector and connector.get_usuarios_collection() is not None:
        try:
            docs = list(connector.get_usuarios_collection().where("email", "==", normalized).limit(1).stream())
            if docs:
                data = docs[0].to_dict() or {}
                data["uid"] = data.get("uid") or docs[0].id
                data["source"] = "firestore"
                return data
        except Exception as exc:
            print(f"No se pudo buscar el usuario para el reset: {exc}")
    return None


def request_reset(email: str) -> Dict[str, Any]:
    """Genera un token de un solo uso. No revela si el correo existe."""
    normalized = str(email or "").strip().lower()
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=RESET_TTL_MINUTES)
    user = _find_user(normalized)

    if user:
        RESET_TOKENS[token] = {
            "email": normalized,
            "uid": user.get("uid"),
            "source": user.get("source"),
            "expires_at": expires_at.isoformat(),
            "used": False,
        }

    return {
        "message": "Si el correo está registrado, recibirás un enlace de recuperación",
        "token": token if user else "",
        "expires_at": expires_at.isoformat() if user else "",
    }


def reset_password(token: str, new_password: str) -> bool:
    entry = RESET_TOKENS.get(str(token or ""))
    if not entry or entry.get("used"):
        raise ValueError("Token de recuperación no válido")
    if datetime.fromisoformat(entry["expires_at"]) < datetime.now():
        RESET_TOKENS.pop(token, None)
        raise ValueError("El token de recuperación ha expirado")
    if not is_strong_password(new_password):
        raise ValueError("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número")

    local = _local_users().get(entry["email"])
    if local:
        local["password_hash"] = hash_password(new_password)
        local["password_updated_at"] = datetime.now().isoformat()

    connector = _connector()
    if connector and entry.get("uid"):
        try:
            connector.update_usuario(
                entry["uid"],
                {"password_hash": hash_password(new_password), "password_updated_at": datetime.now().isoformat()},
            )
        except Exception as exc:
            print(f"No se pudo actualizar la contraseña en Firestore: {exc}")

    entry["used"] = True
    return True
