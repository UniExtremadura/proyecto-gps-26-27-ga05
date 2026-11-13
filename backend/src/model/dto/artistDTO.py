"""DTO de artista."""
from typing import Any, Dict


class artistDTO:
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def set_data(self, data: Dict[str, Any]) -> "artistDTO":
        self._data = dict(data or {})
        return self

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def to_json(self) -> str:
        import json

        return json.dumps(self.to_dict())
