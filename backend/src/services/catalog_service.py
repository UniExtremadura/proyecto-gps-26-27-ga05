"""Servicio de catálogo con búsqueda y filtros (TK-006-1)."""
import json
from datetime import datetime
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from model.model import Model

SAMPLE_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "riverland-fest-2026",
        "name": "Riverland Fest 2026",
        "title": "Riverland Fest 2026",
        "genre": "indie",
        "location": "Pravia, Asturias",
        "date": "2026-06-20",
        "ticket_price": 60,
        "available_tickets": 1200,
        "image": "./assets/img/riverland.png",
        "description": "Festival de música y cultura en el corazón de Asturias.",
    },
    {
        "id": "boombastic-costa-del-sol-2026",
        "name": "Boombastic Costa del Sol 2026",
        "title": "Boombastic Costa del Sol 2026",
        "genre": "urban",
        "location": "Torre del Mar, Málaga",
        "date": "2026-07-12",
        "ticket_price": 65,
        "available_tickets": 900,
        "image": "./assets/img/boombastic.jpg",
        "description": "Festival de playa con el mejor ambiente del verano.",
    },
    {
        "id": "zevra-experience-2026",
        "name": "Zevra Experience 2026",
        "title": "Zevra Experience 2026",
        "genre": "electronic",
        "location": "Valencia",
        "date": "2026-08-01",
        "ticket_price": 55,
        "available_tickets": 700,
        "image": "./assets/img/zevra.jpg",
        "description": "Una experiencia inmersiva de música electrónica.",
    },
]


def _model() -> Model:
    return Model(factory=FirebaseDAOFactory())


def load_events() -> List[Dict[str, Any]]:
    """Carga eventos desde Firestore y cae a datos de ejemplo si falla."""
    try:
        events = json.loads(_model().get_all_eventos())
        if isinstance(events, list) and events:
            return events
    except Exception as exc:
        print(f"Catalog fallback: {exc}")
    return [dict(item) for item in SAMPLE_EVENTS]


def _matches(event: Dict[str, Any], q: str, genre: str, location: str, date_from: str, date_to: str) -> bool:
    haystack = " ".join(
        str(event.get(field, "")) for field in ("name", "title", "description", "genre", "location", "artist")
    ).lower()
    if q and q.lower() not in haystack:
        return False
    if genre and genre.lower() not in str(event.get("genre", "")).lower():
        return False
    if location and location.lower() not in str(event.get("location", event.get("loc", ""))).lower():
        return False
    event_date = str(event.get("date", ""))[:10]
    if date_from and event_date and event_date < date_from:
        return False
    if date_to and event_date and event_date > date_to:
        return False
    return True


def search_events(
    q: str = "",
    genre: str = "",
    location: str = "",
    date_from: str = "",
    date_to: str = "",
    page: int = 1,
    page_size: int = 12,
) -> Dict[str, Any]:
    """Devuelve una página de eventos filtrados."""
    events = [event for event in load_events() if _matches(event, q, genre, location, date_from, date_to)]
    events.sort(key=lambda event: str(event.get("date", "")))
    page = max(1, int(page or 1))
    page_size = min(50, max(1, int(page_size or 12)))
    start = (page - 1) * page_size
    return {
        "items": events[start : start + page_size],
        "total": len(events),
        "page": page,
        "page_size": page_size,
        "pages": max(1, (len(events) + page_size - 1) // page_size),
    }


def get_event(event_id: str) -> Dict[str, Any] | None:
    for event in load_events():
        if str(event.get("id")) == str(event_id):
            return event
    return None


def catalog_filters() -> Dict[str, Any]:
    events = load_events()
    genres = sorted({str(event.get("genre", "")).strip() for event in events if event.get("genre")})
    locations = sorted({str(event.get("location", event.get("loc", ""))).strip() for event in events if event.get("location") or event.get("loc")})
    return {"genres": genres, "locations": locations, "updated_at": datetime.now().isoformat()}
