"""API de reserva de recintos (TK-009-1)."""
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from security.rbac import require_roles
from services.booking_service import cancel_booking, create_booking, get_venue, list_bookings, list_venues, venue_availability

router = APIRouter(tags=["bookings"])


@router.get("/api/venues")
async def venues():
    return JSONResponse(status_code=200, content={"status": "success", "data": list_venues()})


@router.get("/api/venues/{venue_id}")
async def venue_detail(venue_id: str):
    venue = get_venue(venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return JSONResponse(status_code=200, content={"status": "success", "data": venue})


@router.get("/api/venues/{venue_id}/availability")
async def venue_availability_endpoint(venue_id: str, date: str = Query(...)):
    try:
        return JSONResponse(status_code=200, content={"status": "success", "data": venue_availability(venue_id, date)})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/api/bookings")
async def my_bookings(user: dict = Depends(require_roles("proveedor", "admin"))):
    return JSONResponse(status_code=200, content={"status": "success", "data": list_bookings(user["uid"])})


@router.post("/api/bookings")
async def new_booking(data: dict = Body(...), user: dict = Depends(require_roles("proveedor", "admin"))):
    try:
        booking = create_booking(data, user["uid"])
        return JSONResponse(status_code=201, content={"status": "success", "message": "Reserva creada", "data": booking})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/api/bookings/{booking_id}")
async def remove_booking(booking_id: str, user: dict = Depends(require_roles("proveedor", "admin"))):
    try:
        if not cancel_booking(booking_id, user["uid"]):
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return JSONResponse(status_code=200, content={"status": "success", "message": "Reserva cancelada"})
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
@router.get("/api/bookings/history")
async def booking_history_endpoint(
    status: str = Query(""),
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_roles("proveedor", "admin")),
):
    from services.booking_service import booking_history, booking_summary

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "summary": booking_summary(user["uid"]),
            "data": booking_history(user["uid"], status, limit),
        },
    )
