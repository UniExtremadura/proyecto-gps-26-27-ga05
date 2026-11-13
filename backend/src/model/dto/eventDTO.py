"""DTO de evento/festival."""
from typing import Any, Dict


class eventDTO:
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.date = None
        self.location = None
        self.status = "borrador"
        self._data: Dict[str, Any] = {}

    def set_data(self, data: Dict[str, Any]) -> "eventDTO":
        self._data = dict(data or {})
        self.id = self._data.get("id")
        self.name = self._data.get("name") or self._data.get("title")
        self.date = self._data.get("date")
        self.location = self._data.get("location") or self._data.get("loc")
        self.status = self._data.get("status", "borrador")
        return self

    def event_to_dict(self) -> Dict[str, Any]:
        data = dict(self._data)
        if self.id is not None:
            data["id"] = self.id
        return data

    def to_json(self) -> str:
        import json

        return json.dumps(self.event_to_dict())
