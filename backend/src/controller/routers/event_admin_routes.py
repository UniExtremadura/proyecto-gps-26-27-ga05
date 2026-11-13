"""CRUD de eventos para organizadores (TK-008-1)."""
import json

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from model.model import Model
from security.rbac import require_roles
from services.event_admin_service import create_event, delete_event, set_event_status, update_event

router = APIRouter(prefix="/api/admin/events", tags=["event-admin"])


@router.get("")
async def list_admin_events(user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    try:
        events = json.loads(Model(factory=FirebaseDAOFactory()).get_all_eventos())
        return JSONResponse(status_code=200, content={"status": "success", "data": events})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudieron cargar los eventos: {exc}")


@router.post("")
async def create_admin_event(data: dict = Body(...), user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    try:
        if not create_event(data):
            raise HTTPException(status_code=500, detail="No se pudo crear el evento")
        return JSONResponse(status_code=201, content={"status": "success", "message": "Evento creado"})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/{event_id}")
async def update_admin_event(event_id: str, data: dict = Body(...), user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    try:
        if not update_event(event_id, data):
            raise HTTPException(status_code=500, detail="No se pudo actualizar el evento")
        return JSONResponse(status_code=200, content={"status": "success", "message": "Evento actualizado"})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{event_id}")
async def delete_admin_event(event_id: str, user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    if not delete_event(event_id):
        raise HTTPException(status_code=500, detail="No se pudo eliminar el evento")
    return JSONResponse(status_code=200, content={"status": "success", "message": "Evento eliminado"})


@router.post("/{event_id}/publish")
async def publish_admin_event(event_id: str, data: dict = Body(default={}), user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    try:
        if not set_event_status(event_id, data.get("status", "publicado")):
            raise HTTPException(status_code=500, detail="No se pudo publicar el evento")
        return JSONResponse(status_code=200, content={"status": "success", "message": "Estado del evento actualizado"})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
