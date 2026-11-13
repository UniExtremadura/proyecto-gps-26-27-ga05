from ....dao.firebase.firebaseConnector import FirebaseConnector
from ....dto.eventDTO import eventDTO
from typing import Any, Dict, List, Optional


class FirebaseEventoDAO:
    def __init__(self, connector: FirebaseConnector) -> None:
        self.connector = connector

    def get_all_eventos(self) -> List[Any]:
        return [eventDTO().set_data(item) for item in self.connector.get_all_eventos()]

    def get_evento_by_id(self, event_id: str) -> Optional[Any]:
        doc = self.connector.get_evento_by_id(event_id)
        if doc is None or not getattr(doc, "exists", False):
            return None
        data = doc.to_dict() or {}
        data["id"] = data.get("id") or doc.id
        return eventDTO().set_data(data)

    def create_evento(self, event_data: Dict[str, Any]) -> bool:
        return bool(self.connector.create_evento(event_data))

    def update_evento(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        return self.connector.update_evento(event_id, event_data)

    def delete_evento(self, event_id: str) -> bool:
        return self.connector.delete_evento(event_id)
