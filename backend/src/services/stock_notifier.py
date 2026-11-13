"""Notificaciones de stock bajo (TK-011-2)."""
from typing import Any, Dict

from services.mailer import send_stock_alert
from services.stock_service import get_stock

DEFAULT_ALERT_EMAIL = "proveedor.demo@subsonicfest.com"


def notify_if_low_stock(product_id: str, recipient: str = "") -> Dict[str, Any]:
    stock = get_stock(product_id)
    if not stock:
        return {"notified": False, "reason": "Producto no encontrado"}
    if not stock["low_stock"]:
        return {"notified": False, "reason": "Stock por encima del umbral"}

    sent = send_stock_alert(
        recipient or DEFAULT_ALERT_EMAIL,
        stock.get("name") or product_id,
        stock["stock"],
        stock["min_stock"],
    )
    return {"notified": sent, "stock": stock}
