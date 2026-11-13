from ....dao.firebase.firebaseConnector import FirebaseConnector
from ....dto.orderDTO import orderDTO
from typing import Any, Dict, List, Optional


class FirebasePedidoDAO:
    def __init__(self, connector: FirebaseConnector) -> None:
        self.connector = connector

    def _dto(self, data: Dict[str, Any]) -> orderDTO:
        return orderDTO().set_data(data or {})

    def get_all_pedidos(self) -> List[Any]:
        return [self._dto(item) for item in self.connector.get_all_pedidos()]

    def get_pedidos_by_uid(self, uid: str) -> List[Any]:
        return [self._dto(item) for item in self.connector.get_pedidos_by_uid(uid)]

    def get_pedido_by_id(self, order_id: str) -> Optional[Any]:
        doc = self.connector.get_pedido_by_id(order_id)
        if doc is None or not getattr(doc, "exists", False):
            return None
        data = doc.to_dict() or {}
        data["id"] = data.get("id") or doc.id
        return self._dto(data)

    def create_pedido(self, order_data: Dict[str, Any]) -> bool:
        return bool(self.connector.create_pedido(order_data))

    def update_pedido(self, order_id: str, order_data: Dict[str, Any]) -> bool:
        return self.connector.update_pedido(order_id, order_data)
