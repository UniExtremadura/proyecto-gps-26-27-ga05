from ....dao.interfaceUsuarioDAO import InterfaceUsuarioDAO
from ....dto.userDTO import userDTO
from typing import Any, Optional


class FirebaseUsuarioDAO(InterfaceUsuarioDAO):
    def __init__(self, connector: Any) -> None:
        self.connector = connector

    def get_usuario(self, uid: str) -> Optional[Any]:
        user = userDTO()
        try:
            doc = self.connector.get_usuario_by_uid(uid)
            if doc is not None and getattr(doc, "exists", False):
                data = doc.to_dict() or {}
                data["uid"] = data.get("uid") or doc.id
                return user.set_data(data)
        except Exception as exc:
            print(f"Error getting user: {exc}")
        return user
