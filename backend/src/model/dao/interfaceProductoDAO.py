from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class InterfaceProductoDAO(ABC):
    @abstractmethod
    def get_all_productos(self) -> List[Any]:
        pass

    @abstractmethod
    def get_producto_by_id(self, product_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def create_producto(self, producto_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def update_producto(self, product_id: str, producto_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_producto(self, product_id: str) -> bool:
        pass
