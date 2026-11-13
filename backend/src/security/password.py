"""Hash y validación de contraseñas con Bcrypt."""
import re

import bcrypt

BCRYPT_ROUNDS = 10


def hash_password(password: str) -> str:
    """Devuelve el hash Bcrypt de una contraseña en texto plano."""
    raw = str(password or "").encode("utf-8")
    return bcrypt.hashpw(raw, bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Comprueba una contraseña contra un hash Bcrypt."""
    try:
        return bcrypt.checkpw(str(password or "").encode("utf-8"), str(hashed).encode("utf-8"))
    except (ValueError, TypeError):
        return False


def is_strong_password(password: str) -> bool:
    """Regla US-001: mínimo 8 caracteres, una mayúscula y un número."""
    text = str(password or "")
    return (
        len(text) >= 8
        and bool(re.search(r"[A-ZÁÉÍÓÚÜÑ]", text))
        and bool(re.search(r"\d", text))
    )
