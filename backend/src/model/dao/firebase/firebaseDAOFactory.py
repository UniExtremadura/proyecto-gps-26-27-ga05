"""Factoría de DAOs.

Mantiene el nombre histórico ``FirebaseDAOFactory`` para no romper las
importaciones existentes, pero devuelve DAOs respaldados por el conector local
de MongoDB.
"""
from typing import Any

from ...factory.interfaceDAOFactory import InterfaceDAOFactory
from .collection.firebaseArtistaDAO import FirebaseArtistaDAO
from .collection.firebaseEventoDAO import FirebaseEventoDAO
from .collection.firebasePedidoDAO import FirebasePedidoDAO
from .collection.firebaseProductoDAO import FirebaseProductoDAO
from .collection.firebaseUsuarioDAO import FirebaseUsuarioDAO
from .firebaseConnector import FirebaseConnector


class FirebaseDAOFactory(InterfaceDAOFactory):
    def __init__(self) -> None:
        self.connector = FirebaseConnector()

    def getUsuarioDAO(self, uid: str) -> Any:
        return FirebaseUsuarioDAO(self.connector)

    def getPedidosDAO(self) -> Any:
        return FirebasePedidoDAO(self.connector)

    def getProductosDAO(self) -> Any:
        return FirebaseProductoDAO(self.connector)

    def getEventosDAO(self) -> Any:
        return FirebaseEventoDAO(self.connector)

    def getArtistasDAO(self) -> Any:
        return FirebaseArtistaDAO(self.connector)


_factory: FirebaseDAOFactory | None = None


def get_factory() -> FirebaseDAOFactory:
    """Devuelve una factoría compartida para no abrir conexiones de más."""
    global _factory
    if _factory is None:
        _factory = FirebaseDAOFactory()
    return _factory


def get_connector() -> FirebaseConnector:
    return get_factory().connector
