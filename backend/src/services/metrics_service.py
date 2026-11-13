"""Agregación de métricas y ventas (TK-013-1)."""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def _orders() -> List[Dict[str, Any]]:
    connector = _connector()
    orders: List[Dict[str, Any]] = []
    if connector and connector.get_db():
        try:
            for doc in connector.get_db().collection("pedidos").stream():
                data = doc.to_dict() or {}
                data["id"] = data.get("id") or doc.id
                orders.append(data)
        except Exception as exc:
            print(f"No se pudieron cargar los pedidos: {exc}")
    return orders


def _parse_date(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(text[:10], fmt)
            except ValueError:
                continue
    return None


def _order_amount(order: Dict[str, Any]) -> float:
    for key in ("total", "amount", "total_amount", "subtotal"):
        if order.get(key) is not None:
            try:
                return float(order[key])
            except (TypeError, ValueError):
                continue
    return 0.0


def _order_units(order: Dict[str, Any]) -> int:
    items = order.get("items") or order.get("products") or []
    if isinstance(items, dict):
        items = list(items.values())
    units = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            units += int(item.get("quantity", item.get("units", 1)) or 0)
        except (TypeError, ValueError):
            continue
    return units or int(order.get("units", 1) or 1)


def _filter_period(orders: List[Dict[str, Any]], days: int) -> List[Dict[str, Any]]:
    if days <= 0:
        return orders
    threshold = datetime.now() - timedelta(days=days)
    result = []
    for order in orders:
        created = _parse_date(order.get("created_at") or order.get("date") or order.get("fecha"))
        if created is None or created >= threshold:
            result.append(order)
    return result


def sales_metrics(provider_uid: str = "", days: int = 30) -> Dict[str, Any]:
    orders = _filter_period(_orders(), days)
    if provider_uid:
        orders = [
            order
            for order in orders
            if str(order.get("provider_uid") or order.get("owner_uid") or "") in ("", str(provider_uid))
        ]

    by_product: Dict[str, Dict[str, Any]] = {}
    by_day: Dict[str, Dict[str, Any]] = {}
    by_status: Dict[str, int] = {}
    total_revenue = 0.0
    total_units = 0

    for order in orders:
        amount = _order_amount(order)
        units = _order_units(order)
        total_revenue += amount
        total_units += units

        status = str(order.get("status") or "pendiente").lower()
        by_status[status] = by_status.get(status, 0) + 1

        day = (_parse_date(order.get("created_at") or order.get("date")) or datetime.now()).strftime("%Y-%m-%d")
        day_entry = by_day.setdefault(day, {"date": day, "revenue": 0.0, "orders": 0})
        day_entry["revenue"] += amount
        day_entry["orders"] += 1

        items = order.get("items") or order.get("products") or []
        if isinstance(items, dict):
            items = list(items.values())
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or item.get("product_name") or "Producto"
            quantity = int(item.get("quantity", item.get("units", 1)) or 0)
            price = float(item.get("price", item.get("unit_price", 0)) or 0)
            entry = by_product.setdefault(name, {"product": name, "units": 0, "revenue": 0.0})
            entry["units"] += quantity
            entry["revenue"] += price * quantity

    order_count = len(orders)
    return {
        "period_days": days,
        "summary": {
            "revenue": round(total_revenue, 2),
            "orders": order_count,
            "units": total_units,
            "average_ticket": round(total_revenue / order_count, 2) if order_count else 0.0,
        },
        "by_day": sorted(by_day.values(), key=lambda item: item["date"]),
        "by_product": sorted(by_product.values(), key=lambda item: item["revenue"], reverse=True),
        "by_status": by_status,
    }


def sales_csv(provider_uid: str = "", days: int = 30) -> str:
    data = sales_metrics(provider_uid, days)
    lines = ["fecha,pedidos,ingresos"]
    for day in data["by_day"]:
        lines.append(f"{day['date']},{day['orders']},{day['revenue']}")
    lines.append("")
    lines.append("producto,unidades,ingresos")
    for product in data["by_product"]:
        lines.append(f"{product['product']},{product['units']},{product['revenue']}")
    return "\n".join(lines)
