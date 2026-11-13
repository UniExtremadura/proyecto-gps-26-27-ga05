"""Endpoints de moderación para administradores (TK-014-1)."""
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from security.rbac import require_roles
from services.moderation_service import list_users, moderate_event, reactivate_user, suspend_user

router = APIRouter(prefix="/api/admin", tags=["admin-moderation"])


@router.get("/users")
async def admin_users(user: dict = Depends(require_roles("admin"))):
    return JSONResponse(status_code=200, content={"status": "success", "data": list_users()})


@router.post("/users/{uid}/suspend")
async def suspend_account(uid: str, data: dict = Body(default={}), user: dict = Depends(require_roles("admin"))):
    suspend_user(uid, data.get("reason", ""))
    return JSONResponse(status_code=200, content={"status": "success", "message": "Cuenta suspendida"})


@router.post("/users/{uid}/reactivate")
async def reactivate_account(uid: str, user: dict = Depends(require_roles("admin"))):
    reactivate_user(uid)
    return JSONResponse(status_code=200, content={"status": "success", "message": "Cuenta reactivada"})


@router.post("/events/{event_id}/moderate")
async def moderate_admin_event(event_id: str, data: dict = Body(...), user: dict = Depends(require_roles("admin"))):
    try:
        moderate_event(event_id, data.get("decision", ""), data.get("reason", ""))
        return JSONResponse(status_code=200, content={"status": "success", "message": "Evento moderado"})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
