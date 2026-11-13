"""DTO de pedido."""
from typing import Any, Dict


class orderDTO:
    def __init__(self) -> None:
        self.id = None
        self.uid = None
        self.items = []
        self.total = 0
        self.status = "pendiente"
        self.created_at = None
        self.updated_at = None
        self._extra: Dict[str, Any] = {}

    def set_data(self, data: Dict[str, Any]) -> "orderDTO":
        extra = dict(data or {})
        self.id = extra.pop("id", self.id)
        self.uid = extra.pop("uid", self.uid)
        self.items = extra.pop("items", self.items)
        self.total = extra.pop("total", self.total)
        self.status = extra.pop("status", self.status)
        self.created_at = extra.pop("created_at", self.created_at)
        self.updated_at = extra.pop("updated_at", self.updated_at)
        self._extra = extra
        return self

    def order_to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "uid": self.uid,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        data.update(self._extra)
        return data

    def to_json(self) -> str:
        import json

        return json.dumps(self.order_to_dict())
