"""Lógica de stock y umbral mínimo de unidades (TK-011-1)."""
from datetime import datetime
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory

DEFAULT_MIN_STOCK = 5
STOCK_OVERRIDES: Dict[str, Dict[str, Any]] = {}


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def _products() -> List[Dict[str, Any]]:
    connector = _connector()
    products = []
    if connector and connector.get_productos_collection() is not None:
        try:
            for doc in connector.get_productos_collection().stream():
                data = doc.to_dict() or {}
                data["id"] = data.get("id") or doc.id
                products.append(data)
        except Exception as exc:
            print(f"No se pudieron cargar productos: {exc}")
    for product_id, override in STOCK_OVERRIDES.items():
        for product in products:
            if product.get("id") == product_id:
                product.update(override)
    return products


def get_stock(product_id: str) -> Dict[str, Any] | None:
    for product in _products():
        if str(product.get("id")) == str(product_id):
            return {
                "product_id": product_id,
                "name": product.get("name", ""),
                "stock": int(product.get("stock", 0) or 0),
                "min_stock": int(product.get("min_stock", DEFAULT_MIN_STOCK) or DEFAULT_MIN_STOCK),
                "low_stock": int(product.get("stock", 0) or 0) <= int(product.get("min_stock", DEFAULT_MIN_STOCK) or DEFAULT_MIN_STOCK),
            }
    return None


def list_stock() -> List[Dict[str, Any]]:
    result = []
    for product in _products():
        stock = int(product.get("stock", 0) or 0)
        min_stock = int(product.get("min_stock", DEFAULT_MIN_STOCK) or DEFAULT_MIN_STOCK)
        result.append(
            {
                "product_id": product.get("id"),
                "name": product.get("name", ""),
                "stock": stock,
                "min_stock": min_stock,
                "low_stock": stock <= min_stock,
            }
        )
    return result


def low_stock_alerts() -> List[Dict[str, Any]]:
    return [item for item in list_stock() if item["low_stock"]]


def update_stock(product_id: str, stock: int, min_stock: int = DEFAULT_MIN_STOCK) -> Dict[str, Any]:
    stock = max(0, int(stock))
    min_stock = max(0, int(min_stock))
    payload = {"stock": stock, "min_stock": min_stock, "updated_at": datetime.now().isoformat()}
    STOCK_OVERRIDES[str(product_id)] = payload

    connector = _connector()
    if connector and connector.get_productos_collection() is not None:
        try:
            connector.get_productos_collection().document(str(product_id)).update(payload)
        except Exception as exc:
            print(f"No se pudo actualizar el stock en Firestore: {exc}")

    return {"product_id": product_id, **payload, "low_stock": stock <= min_stock}


def decrement_stock(product_id: str, quantity: int = 1) -> Dict[str, Any]:
    current = get_stock(product_id)
    if not current:
        raise ValueError("Producto no encontrado")
    quantity = max(1, int(quantity))
    if current["stock"] < quantity:
        raise ValueError("Stock insuficiente")
    updated = update_stock(product_id, current["stock"] - quantity, current["min_stock"])
    # TK-011-2 hook: notificar si se cruza el umbral.
    return updated
