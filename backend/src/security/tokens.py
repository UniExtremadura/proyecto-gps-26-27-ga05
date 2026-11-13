"""Emisión, validación y revocación de tokens JWT."""
from datetime import datetime, timedelta, timezone
from typing import Set

from jose import JWTError, jwt

from config.config import JWT_ALGORITHM, JWT_SECRET, TOKEN_EXPIRY_HOURS

# Lista de revocación en memoria (suficiente para el entorno local).
REVOKED_TOKENS: Set[str] = set()


def create_access_token(subject: str, role: str, email: str) -> str:
    """Crea un JWT con el uid, rol y email del usuario."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "uid": str(subject),
        "role": str(role or "cliente"),
        "email": str(email or ""),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=TOKEN_EXPIRY_HOURS)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Valida firma y expiración. Lanza JWTError si el token no es válido."""
    if token in REVOKED_TOKENS:
        raise JWTError("Token revocado")
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def revoke_token(token: str) -> None:
    """Añade un token a la lista de revocación (logout)."""
    if token:
        REVOKED_TOKENS.add(token)


def is_token_revoked(token: str) -> bool:
    return token in REVOKED_TOKENS
