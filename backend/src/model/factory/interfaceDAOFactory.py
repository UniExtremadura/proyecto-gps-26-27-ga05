from abc import ABC, abstractmethod
from typing import Any

class InterfaceDAOFactory(ABC):
    @abstractmethod
    def getUsuarioDAO(self, uid: str) -> Any:
        pass