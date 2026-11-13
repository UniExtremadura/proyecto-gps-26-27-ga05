"""Lógica de administración de eventos y entradas (TK-008-1)."""
from datetime import datetime
from typing import Any, Dict

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from model.model import Model


def _model() -> Model:
    return Model(factory=FirebaseDAOFactory())


def validate_event(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valida y normaliza los campos mínimos de un evento."""
    name = str(data.get("name") or data.get("title") or "").strip()
    date = str(data.get("date") or "").strip()
    location = str(data.get("location") or data.get("loc") or "").strip()
    if not name:
        raise ValueError("El nombre del evento es obligatorio")
    if not date:
        raise ValueError("La fecha del evento es obligatoria")
    if not location:
        raise ValueError("La ubicación del evento es obligatoria")

    ticket_price = data.get("ticket_price", data.get("price", 0))
    available_tickets = data.get("available_tickets", data.get("stock", 0))
    try:
        ticket_price = float(ticket_price or 0)
        available_tickets = int(available_tickets or 0)
    except (TypeError, ValueError):
        raise ValueError("Precio o aforo no válidos")

    return {
        **data,
        "name": name,
        "title": data.get("title") or name,
        "date": date,
        "location": location,
        "loc": location,
        "ticket_price": ticket_price,
        "available_tickets": available_tickets,
        "status": data.get("status") or "borrador",
        "updated_at": datetime.now().isoformat(),
    }


def create_event(data: Dict[str, Any]) -> bool:
    event = validate_event(data)
    event["created_at"] = datetime.now().isoformat()
    return _model().create_evento(event)


def update_event(event_id: str, data: Dict[str, Any]) -> bool:
    event = validate_event(data)
    return _model().update_evento(event_id, event)


def delete_event(event_id: str) -> bool:
    return _model().delete_evento(event_id)


def set_event_status(event_id: str, status: str) -> bool:
    normalized = str(status or "").strip().lower()
    if normalized not in {"borrador", "publicado", "archivado"}:
        raise ValueError("Estado de evento no válido")
    return _model().update_evento(event_id, {"status": normalized, "updated_at": datetime.now().isoformat()})
