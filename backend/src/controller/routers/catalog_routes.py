"""API pública de catálogo (TK-006-1)."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from security.rbac import require_roles
from services.cache_service import catalog_cache
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
    cache_key = f"catalog:{q}:{genre}:{location}:{date_from}:{date_to}:{page}:{page_size}"
    data = catalog_cache.get_or_set(
        cache_key,
        lambda: search_events(q, genre, location, date_from, date_to, page, page_size),
    )
    return JSONResponse(
        status_code=200,
        content={"status": "success", "cached": True, "data": data},
    )


@router.get("/events/{event_id}")
async def catalog_event_detail(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return JSONResponse(status_code=200, content={"status": "success", "data": event})


@router.get("/filters")
async def catalog_available_filters():
    data = catalog_cache.get_or_set("catalog:filters", catalog_filters, ttl=120)
    return JSONResponse(status_code=200, content={"status": "success", "data": data})


@router.get("/cache/stats")
async def catalog_cache_stats(user: dict = Depends(require_roles("admin", "gestor"))):
    return JSONResponse(status_code=200, content={"status": "success", "data": catalog_cache.stats()})


@router.post("/cache/clear")
async def catalog_cache_clear(user: dict = Depends(require_roles("admin", "gestor"))):
    catalog_cache.invalidate("catalog:")
    return JSONResponse(status_code=200, content={"status": "success", "message": "Caché de catálogo invalidada"})
