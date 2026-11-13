"""API de reinicio de contraseña (TK-005-1)."""
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse

from services.password_reset_service import request_reset, reset_password

router = APIRouter(prefix="/api/auth/password", tags=["password-reset"])


@router.post("/request")
async def password_reset_request(data: dict = Body(...)):
    email = (data.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="El correo electrónico es obligatorio")
    return JSONResponse(status_code=200, content={"status": "success", **request_reset(email)})


@router.post("/reset")
async def password_reset_confirm(data: dict = Body(...)):
    try:
        reset_password(data.get("token", ""), data.get("password", ""))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return JSONResponse(status_code=200, content={"status": "success", "message": "Contraseña actualizada"})
