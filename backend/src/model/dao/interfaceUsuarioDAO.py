from abc import ABC, abstractmethod
from typing import Any, Optional


class InterfaceUsuarioDAO(ABC):
    @abstractmethod
    def get_usuario(self, uid: str) -> Optional[Any]:
        pass
