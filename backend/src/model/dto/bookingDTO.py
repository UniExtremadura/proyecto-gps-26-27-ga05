"""DTO de reservas de recintos (TK-009-1)."""
import json


class bookingDTO:
    def __init__(self):
        self.id = None
        self.provider_uid = None
        self.venue_id = None
        self.space_id = None
        self.event_id = None
        self.date = None
        self.start_time = None
        self.end_time = None
        self.status = "pendiente"
        self.price = 0
        self.notes = ""
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "provider_uid": self.provider_uid,
            "venue_id": self.venue_id,
            "space_id": self.space_id,
            "event_id": self.event_id,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "price": self.price,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_json(self):
        return json.dumps(self.to_dict())
