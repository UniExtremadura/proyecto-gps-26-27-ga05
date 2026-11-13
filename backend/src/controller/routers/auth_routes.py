"""Endpoints de autenticación local con JWT (TK-001-1)."""
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from jose import JWTError

from config.config import ERROR_MESSAGES, SUCCESS_MESSAGES
from model.roles import normalize_role
from security.password import hash_password, is_strong_password, verify_password
from security.rbac import get_current_user
from security.tokens import create_access_token, decode_access_token, revoke_token
from services import user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

PUBLIC_ROLES = {"cliente", "proveedor"}


def _public(user: Dict[str, Any]) -> Dict[str, Any]:
    return user_service.public_user(user)


def _issue_token(user: Dict[str, Any]) -> str:
    return create_access_token(user["uid"], user.get("role", "cliente"), user.get("email", ""))


def _auth_response(user: Dict[str, Any], status_code: int = 200, message: str = SUCCESS_MESSAGES["login_success"]):
    token = _issue_token(user)
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "token": token,
            "sessionToken": token,
            "user": _public(user),
        },
    )


def _register_user(data: Dict[str, Any]) -> Dict[str, Any]:
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    name = str(data.get("name") or data.get("nombre") or "").strip()

    if not email or not password or not name:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_email"])
    if not is_strong_password(password):
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_password"])
    if user_service.email_exists(email):
        raise HTTPException(status_code=409, detail=ERROR_MESSAGES["email_already_registered"])

    requested_role = normalize_role(data.get("role") or "cliente")
    if requested_role not in PUBLIC_ROLES:
        requested_role = "cliente"

    uid = f"local-{uuid4().hex[:12]}"
    user: Dict[str, Any] = {
        "uid": uid,
        "email": email,
        "name": name,
        "role": requested_role,
        "suspended": False,
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "profile_image_url": str(data.get("profile_image_url") or "").strip(),
        "address": str(data.get("address") or "").strip(),
        "postal_code": str(data.get("postal_code") or "").strip(),
        "city": str(data.get("city") or "").strip(),
        "country": str(data.get("country") or "").strip(),
    }
    if requested_role == "proveedor":
        user["company_name"] = str(data.get("company_name") or name).strip()
        user["business_area"] = str(data.get("business_area") or "").strip()
        user["card_number"] = str(data.get("card_number") or "").strip()

    if not user_service.create_user(uid, user):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return user


def _login_user(email: str, password: str) -> Dict[str, Any]:
    normalized = str(email or "").strip().lower()
    user = user_service.find_user_by_email(normalized)
    # Mensaje genérico para no revelar si falla el correo o la contraseña.
    if not user or not verify_password(password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail=ERROR_MESSAGES["invalid_credentials"])
    if user.get("suspended"):
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["suspended"])
    user_service.update_user(user["uid"], {"last_login_at": datetime.now().isoformat()})
    user = user_service.find_user_by_email(normalized) or user
    return user


@router.post("/local/register")
@router.post("/register")
async def register(data: dict = Body(...)):
    user = _register_user(data)
    return _auth_response(user, status_code=201, message=SUCCESS_MESSAGES["register_success"])


@router.post("/local/login")
@router.post("/login")
@router.post("/login-basic")
async def login(data: dict = Body(...)):
    email = data.get("email") or data.get("username") or ""
    password = data.get("password") or ""
    if not email or not password:
        raise HTTPException(status_code=400, detail="Credenciales requeridas")
    user = _login_user(str(email), str(password))
    return _auth_response(user)


@router.get("/local/me")
@router.get("/me")
async def me(request: Request):
    token = ""
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        token = header[7:].strip()
    if not token:
        raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
    try:
        claims = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user = user_service.get_user(claims.get("uid") or claims.get("sub") or "")
    if not user:
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["user_not_found"])
    return JSONResponse(status_code=200, content={"status": "success", "user": _public(user)})


@router.post("/local/logout")
@router.post("/logout")
async def logout(request: Request):
    token = ""
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        token = header[7:].strip()
    revoke_token(token)
    response = JSONResponse(status_code=200, content={"status": "success", "message": "Sesión cerrada"})
    response.delete_cookie("session")
    return response


@router.get("/check_email")
@router.get("/check-email")
async def check_email(email: Optional[str] = Query(None)):
    normalized = str(email or "").strip().lower()
    exists = bool(normalized and user_service.email_exists(normalized))
    return JSONResponse(status_code=200, content={"status": "success", "exists": exists})


@router.post("/google-register")
async def google_register(data: dict = Body(...)):
    """Vincula/crea la cuenta de un perfil OAuth ya validado.

    El frontend puede enviar directamente los datos del perfil (modo demo) o un
    ``id_token`` de Google para que el endpoint de OAuth lo valide.
    """
    from security.oauth import OAuthError, normalize_oauth_profile, verify_google_id_token

    token = data.get("token") or data.get("id_token")
    if token:
        try:
            profile = verify_google_id_token(token)
        except OAuthError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
    else:
        profile = {
            "provider": "google",
            "uid": data.get("uid") or data.get("sub") or f"google-{uuid4().hex[:10]}",
            "email": data.get("email") or "",
            "name": data.get("name") or "",
            "picture": data.get("profile_image_url") or data.get("picture") or "",
        }
    profile["role"] = data.get("role", "cliente")
    normalized = normalize_oauth_profile(profile)
    if not normalized.get("email"):
        raise HTTPException(status_code=400, detail="El proveedor no devolvió un email")

    user = user_service.find_user_by_email(normalized["email"])
    if user and user.get("suspended"):
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["suspended"])
    if not user:
        uid = normalized["uid"] or f"oauth-{uuid4().hex[:12]}"
        user = {
            "uid": uid,
            "email": normalized["email"],
            "name": normalized.get("name") or normalized["email"].split("@")[0],
            "role": normalize_role(normalized.get("role", "cliente")),
            "provider": normalized.get("provider", "google"),
            "profile_image_url": normalized.get("profile_image_url", ""),
            "suspended": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        user_service.create_user(uid, user)
        user = user_service.get_user(uid) or user
    return _auth_response(user, message="Inicio de sesión externo correcto")


@router.get("/local/roles")
async def current_roles(user: dict = None):
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "roles": ["visitante", "cliente", "proveedor", "gestor", "admin"],
        },
    )
