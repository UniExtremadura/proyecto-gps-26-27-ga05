from ....dao.interfaceUsuarioDAO import InterfaceUsuarioDAO
from ....dto.userDTO import userDTO
from typing import Optional, Any

class FirebaseUsuarioDAO(InterfaceUsuarioDAO):
    def __init__(self, user_doc: Any) -> None:
        self.user_doc = user_doc

    def get_usuario(self, uid: str) -> Optional[Any]:
        user = userDTO()
        if self.user_doc and self.user_doc.exists:
            data = self.user_doc.to_dict()
            user.set_uid(self.user_doc.id)
            user.set_name(data.get("name", ""))
            user.set_email(data.get("email", ""))
            user.set_role(data.get("role", ""))
        return user