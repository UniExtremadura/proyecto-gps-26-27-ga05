"""Lógica de reserva de recintos y espacios (TK-009-1)."""
from datetime import datetime
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory

VENUES: List[Dict[str, Any]] = [
    {
        "id": "recinto-dehesa",
        "name": "Recinto Dehesa Subsonic",
        "city": "Cáceres",
        "capacity": 12000,
        "spaces": [
            {"id": "escenario-principal", "name": "Escenario Principal", "capacity": 8000, "price": 3200},
            {"id": "zona-foodtruck", "name": "Zona Food Truck", "capacity": 1200, "price": 850},
            {"id": "carpa-merch", "name": "Carpa Merchandising", "capacity": 400, "price": 420},
        ],
    },
    {
        "id": "recinto-marina",
        "name": "Marina Sound Park",
        "city": "Valencia",
        "capacity": 6500,
        "spaces": [
            {"id": "main-stage", "name": "Main Stage", "capacity": 5000, "price": 2600},
            {"id": "market-area", "name": "Market Area", "capacity": 900, "price": 600},
        ],
    },
]

# Reservas en memoria para desarrollo y tests.
BOOKINGS: List[Dict[str, Any]] = []


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def list_venues() -> List[Dict[str, Any]]:
    return VENUES


def get_venue(venue_id: str) -> Dict[str, Any] | None:
    for venue in VENUES:
        if venue["id"] == venue_id:
            return venue
    return None


def _bookings_for_date(venue_id: str, date: str) -> List[Dict[str, Any]]:
    return [
        booking
        for booking in BOOKINGS
        if booking.get("venue_id") == venue_id
        and booking.get("date") == date
        and booking.get("status") != "cancelada"
    ]


def venue_availability(venue_id: str, date: str) -> Dict[str, Any]:
    venue = get_venue(venue_id)
    if not venue:
        raise ValueError("Recinto no encontrado")
    reserved = {booking.get("space_id") for booking in _bookings_for_date(venue_id, date)}
    spaces = []
    for space in venue["spaces"]:
        spaces.append({**space, "available": space["id"] not in reserved})
    return {"venue": venue, "date": date, "spaces": spaces}


def _overlaps(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    return start_a < end_b and start_b < end_a


def create_booking(data: Dict[str, Any], provider_uid: str) -> Dict[str, Any]:
    venue_id = str(data.get("venue_id") or "").strip()
    space_id = str(data.get("space_id") or "").strip()
    date = str(data.get("date") or "").strip()
    start_time = str(data.get("start_time") or "10:00").strip()
    end_time = str(data.get("end_time") or "22:00").strip()

    venue = get_venue(venue_id)
    if not venue:
        raise ValueError("Recinto no encontrado")
    space = next((item for item in venue["spaces"] if item["id"] == space_id), None)
    if not space:
        raise ValueError("Espacio no encontrado")
    if not date:
        raise ValueError("La fecha de la reserva es obligatoria")

    for existing in _bookings_for_date(venue_id, date):
        if existing.get("space_id") == space_id and _overlaps(
            start_time, end_time, existing.get("start_time", ""), existing.get("end_time", "")
        ):
            raise ValueError("El espacio ya está reservado en ese horario")

    booking = {
        "id": f"booking-{len(BOOKINGS) + 1}-{int(datetime.now().timestamp())}",
        "provider_uid": provider_uid,
        "venue_id": venue_id,
        "space_id": space_id,
        "event_id": data.get("event_id", ""),
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "status": "confirmada",
        "price": space["price"],
        "notes": str(data.get("notes") or ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    BOOKINGS.append(booking)

    connector = _connector()
    if connector and connector.get_db():
        try:
            connector.get_db().collection("reservas").document(booking["id"]).set(booking)
        except Exception as exc:
            print(f"No se pudo persistir la reserva en Firestore: {exc}")

    return booking


def cancel_booking(booking_id: str, provider_uid: str) -> bool:
    for booking in BOOKINGS:
        if booking["id"] == booking_id:
            if booking.get("provider_uid") != provider_uid:
                raise PermissionError("La reserva pertenece a otro proveedor")
            booking["status"] = "cancelada"
            booking["updated_at"] = datetime.now().isoformat()
            return True
    return False


def list_bookings(provider_uid: str) -> List[Dict[str, Any]]:
    return [booking for booking in BOOKINGS if booking.get("provider_uid") == provider_uid]
