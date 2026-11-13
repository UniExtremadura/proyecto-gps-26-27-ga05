"""Generación y validación de tokens de recuperación (TK-005-1)."""
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from security.password import hash_password, is_strong_password
from services import user_service

RESET_TTL_MINUTES = 15
RESET_TOKENS: Dict[str, Dict[str, Any]] = {}


def _find_user(email: str) -> Dict[str, Any] | None:
    return user_service.find_user_by_email(email)


def request_reset(email: str) -> Dict[str, Any]:
    """Genera un token de un solo uso. No revela si el correo existe."""
    normalized = str(email or "").strip().lower()
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=RESET_TTL_MINUTES)
    user = _find_user(normalized)

    if user:
        # Invalida cualquier token previo del mismo usuario.
        for key, entry in list(RESET_TOKENS.items()):
            if entry.get("email") == normalized:
                RESET_TOKENS.pop(key, None)
        RESET_TOKENS[token] = {
            "email": normalized,
            "uid": user.get("uid"),
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

    user_service.update_user(
        entry["uid"],
        {
            "password_hash": hash_password(new_password),
            "password_updated_at": datetime.now().isoformat(),
        },
    )
    entry["used"] = True
    return True
