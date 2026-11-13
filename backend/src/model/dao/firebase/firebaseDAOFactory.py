from ...factory.interfaceDAOFactory import InterfaceDAOFactory
from .collection.firebaseUsuarioDAO import FirebaseUsuarioDAO
from .firebaseConnector import FirebaseConnector
from typing import Any

class FirebaseDAOFactory(InterfaceDAOFactory):
    def __init__(self) -> None:
        self.connector = FirebaseConnector()

    def getUsuarioDAO(self, uid: str) -> Any:
        return FirebaseUsuarioDAO(self.connector.get_usuario_by_uid(uid))