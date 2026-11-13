"""API pública de catálogo (TK-006-1)."""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from services.catalog_service import catalog_filters, get_event, search_events

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/events")
async def catalog_events(
    q: str = "",
    genre: str = "",
    location: str = "",
    date_from: str = "",
    date_to: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
):
    """Búsqueda de festivales con filtros y paginación."""
    data = search_events(q, genre, location, date_from, date_to, page, page_size)
    return JSONResponse(status_code=200, content={"status": "success", "data": data})


@router.get("/events/{event_id}")
async def catalog_event_detail(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return JSONResponse(status_code=200, content={"status": "success", "data": event})


@router.get("/filters")
async def catalog_available_filters():
    return JSONResponse(status_code=200, content={"status": "success", "data": catalog_filters()})
