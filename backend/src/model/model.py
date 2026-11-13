from .factory.interfaceDAOFactory import InterfaceDAOFactory
from typing import Dict, Any, Optional

class Model:
    def __init__(self, factory: InterfaceDAOFactory):
        self.factory = factory

    def get_usuario(self, uid: str) -> Optional[Any]:
        try:
            usuario_dao = self.factory.getUsuarioDAO(uid)
            return usuario_dao.get_usuario(uid)
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def create_usuario(self, email: str, password: str, nombre: str, rol: str) -> Optional[str]:
        try:
            connector = self.factory.connector
            return connector.create_user(email=email, password=password, display_name=nombre, role=rol)
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None

    def login_usuario(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            connector = self.factory.connector
            return connector.verify_user_password(email=email, password=password)
        except Exception as e:
            print(f"Error en login: {e}")
            return None