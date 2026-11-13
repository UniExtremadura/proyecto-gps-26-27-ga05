from abc import ABC, abstractmethod
from typing import Any


class InterfaceDAOFactory(ABC):
    @abstractmethod
    def getUsuarioDAO(self, uid: str) -> Any:
        pass

    @abstractmethod
    def getPedidosDAO(self) -> Any:
        pass

    @abstractmethod
    def getProductosDAO(self) -> Any:
        pass

    @abstractmethod
    def getEventosDAO(self) -> Any:
        pass

    @abstractmethod
    def getArtistasDAO(self) -> Any:
        pass
