"""Dependencias de autorización basadas en JWT y roles (TK-002-2)."""
from typing import Iterable

from fastapi import HTTPException, Request
from jose import JWTError

from model.roles import has_permission, normalize_role
from security.tokens import decode_access_token


def _extract_token(request: Request) -> str:
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:].strip()
    # Compatibilidad con la cookie de sesión existente.
    return request.cookies.get("session", "")


def get_current_user(request: Request) -> dict:
    """Reconstruye el usuario a partir del JWT o de la cookie de sesión."""
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="No autorizado")

    # La cookie antigua guarda el uid directamente.
    if "." not in token:
        return {"uid": token, "role": "cliente", "email": ""}

    try:
        claims = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return {
        "uid": claims.get("uid") or claims.get("sub"),
        "role": normalize_role(claims.get("role", "cliente")),
        "email": claims.get("email", ""),
    }


def require_roles(*roles: str):
    """Devuelve una dependencia que exige uno de los roles indicados."""
    allowed = {normalize_role(role) for role in roles}

    def dependency(request: Request) -> dict:
        user = get_current_user(request)
        if normalize_role(user.get("role")) not in allowed:
            raise HTTPException(status_code=403, detail="Acceso denegado")
        return user

    return dependency


def require_permission(permission: str):
    """Devuelve una dependencia que exige un permiso concreto."""

    def dependency(request: Request) -> dict:
        user = get_current_user(request)
        if not has_permission(user.get("role", ""), permission):
            raise HTTPException(status_code=403, detail="Acceso denegado")
        return user

    return dependency


def require_any_permission(permissions: Iterable[str]):
    wanted = list(permissions)

    def dependency(request: Request) -> dict:
        user = get_current_user(request)
        if not any(has_permission(user.get("role", ""), permission) for permission in wanted):
            raise HTTPException(status_code=403, detail="Acceso denegado")
        return user

    return dependency
