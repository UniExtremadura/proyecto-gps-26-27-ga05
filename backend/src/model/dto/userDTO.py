"""DTO de usuario."""
from typing import Any, Dict, Optional


class userDTO:
    def __init__(self) -> None:
        self.uid: Optional[str] = None
        self.email: Optional[str] = None
        self.name: Optional[str] = None
        self.role: Optional[str] = None
        self.suspended: bool = False
        self._extra: Dict[str, Any] = {}

    def is_Empty(self) -> bool:
        return self.uid is None and self.email is None

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role

    def set_data(self, data: Dict[str, Any]) -> "userDTO":
        """Carga el documento completo y conserva los campos adicionales."""
        extra = dict(data or {})
        self.uid = extra.pop("uid", self.uid)
        self.email = extra.pop("email", self.email)
        self.name = extra.pop("name", self.name)
        self.role = extra.pop("role", self.role)
        self.suspended = bool(extra.pop("suspended", False))
        extra.pop("password_hash", None)
        self._extra = extra
        return self

    def user_to_dict(self) -> Dict[str, Any]:
        data = {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "role": self.role,
        }
        data.update(self._extra)
        data["suspended"] = bool(data.get("suspended", self.suspended))
        return data
