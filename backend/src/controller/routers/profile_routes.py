"""Actualización de perfil y verificación de email (TK-003-1)."""
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from security.crypto import decrypt_field, encrypt_field
from security.rbac import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])

PENDING_EMAIL_CHANGES: Dict[str, Dict[str, Any]] = {}
VERIFICATION_TTL_MINUTES = 15


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def _get_user(uid: str) -> Dict[str, Any]:
    connector = _connector()
    if connector:
        try:
            doc = connector.get_usuario_by_uid(uid)
            if doc and doc.exists:
                data = doc.to_dict() or {}
                data["uid"] = data.get("uid") or uid
                data["address"] = decrypt_field(data.get("address", ""))
                data["phone"] = decrypt_field(data.get("phone", ""))
                return data
        except Exception as exc:
            print(f"No se pudo leer el perfil: {exc}")
    return {"uid": uid, "name": "", "email": "", "address": "", "phone": ""}


def _update_user(uid: str, data: Dict[str, Any]) -> bool:
    connector = _connector()
    if connector:
        try:
            return connector.update_usuario(uid, data)
        except Exception as exc:
            print(f"No se pudo actualizar el perfil: {exc}")
    return True


@router.get("")
async def read_profile(user: dict = Depends(get_current_user)):
    return JSONResponse(status_code=200, content={"status": "success", "user": _get_user(user["uid"])})


@router.put("")
async def update_profile(data: dict = Body(...), user: dict = Depends(get_current_user)):
    uid = user["uid"]
    current = _get_user(uid)
    new_email = (data.get("email") or current.get("email") or "").strip().lower()
    password = str(data.get("password") or "")

    update_data = {
        "name": (data.get("name") or current.get("name") or "").strip(),
        "address": (data.get("address") or current.get("address") or "").strip(),
        "phone": (data.get("phone") or current.get("phone") or "").strip(),
        "city": (data.get("city") or current.get("city") or "").strip(),
        "postal_code": (data.get("postal_code") or current.get("postal_code") or "").strip(),
        "country": (data.get("country") or current.get("country") or "").strip(),
        "profile_image_url": (data.get("profile_image_url") or current.get("profile_image_url") or "").strip(),
        "updated_at": datetime.now().isoformat(),
    }
    if current.get("company_name") or data.get("company_name"):
        update_data["company_name"] = (data.get("company_name") or current.get("company_name") or "").strip()
        update_data["business_area"] = (data.get("business_area") or current.get("business_area") or "").strip()

    if not update_data["name"]:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")

    # Los datos de contacto se cifran en reposo (US-017-AC-03).
    update_data["address"] = encrypt_field(update_data["address"])
    update_data["phone"] = encrypt_field(update_data["phone"])
    email_changed = new_email and new_email != str(current.get("email", "")).lower()
    if email_changed:
        if not password:
            raise HTTPException(status_code=400, detail="Debes introducir tu contraseña actual")
        from services import user_service
        from security.password import verify_password

        stored = user_service.get_user(uid) or {}
        if not verify_password(password, stored.get("password_hash", "")):
            raise HTTPException(status_code=400, detail="La contraseña actual no es correcta")
        from services.user_service import find_user_by_email

        if find_user_by_email(new_email):
            raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado")
        token = secrets.token_urlsafe(32)
        PENDING_EMAIL_CHANGES[uid] = {
            "new_email": new_email,
            "token": token,
            "expires_at": (datetime.now() + timedelta(minutes=VERIFICATION_TTL_MINUTES)).isoformat(),
        }
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Revisa tu nuevo correo para confirmar el cambio",
                "verification_required": True,
                "verification_token": token,
            },
        )

    _update_user(uid, update_data)
    return JSONResponse(status_code=200, content={"status": "success", "message": "Perfil actualizado", "user": {**current, **update_data}})


@router.post("/verify-email")
async def verify_email(data: dict = Body(...), user: dict = Depends(get_current_user)):
    uid = user["uid"]
    pending = PENDING_EMAIL_CHANGES.get(uid)
    if not pending:
        raise HTTPException(status_code=400, detail="No hay un cambio de email pendiente")
    if pending["token"] != data.get("token"):
        raise HTTPException(status_code=400, detail="Token de verificación no válido")
    if datetime.fromisoformat(pending["expires_at"]) < datetime.now():
        PENDING_EMAIL_CHANGES.pop(uid, None)
        raise HTTPException(status_code=400, detail="El enlace de verificación ha expirado")

    _update_user(uid, {"email": pending["new_email"], "updated_at": datetime.now().isoformat()})
    PENDING_EMAIL_CHANGES.pop(uid, None)
    return JSONResponse(status_code=200, content={"status": "success", "message": "Correo actualizado"})
