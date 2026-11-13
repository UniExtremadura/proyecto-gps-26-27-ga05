"""Métricas globales de la plataforma (TK-015-1)."""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def _documents(collection: str) -> List[Dict[str, Any]]:
    connector = _connector()
    items: List[Dict[str, Any]] = []
    if connector and connector.get_db():
        try:
            for doc in connector.get_db().collection(collection).stream():
                data = doc.to_dict() or {}
                data["id"] = data.get("id") or doc.id
                items.append(data)
        except Exception as exc:
            print(f"No se pudo leer la colección {collection}: {exc}")
    return items


def _parse(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    text = str(value or "").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _amount(order: Dict[str, Any]) -> float:
    for key in ("total", "amount", "total_amount"):
        if order.get(key) is not None:
            try:
                return float(order[key])
            except (TypeError, ValueError):
                continue
    return 0.0


def global_metrics(days: int = 30) -> Dict[str, Any]:
    threshold = datetime.now() - timedelta(days=days) if days > 0 else None

    users = _documents("usuarios")
    events = _documents("eventos")
    orders = _documents("pedidos")

    def in_period(item: Dict[str, Any]) -> bool:
        if threshold is None:
            return True
        created = _parse(item.get("created_at") or item.get("date") or item.get("fecha"))
        return created is None or created >= threshold

    orders = [order for order in orders if in_period(order)]
    events = [event for event in events if in_period(event)]

    merch_revenue = round(sum(_amount(order) for order in orders), 2)
    ticket_revenue = 0.0
    occupancy_samples = []
    by_festival: Dict[str, Dict[str, Any]] = {}

    for event in events:
        name = event.get("name") or event.get("title") or event.get("id") or "Festival"
        capacity = float(event.get("capacity") or event.get("aforo") or 0)
        sold = float(event.get("tickets_sold") or event.get("sold") or 0)
        price = float(event.get("ticket_price") or event.get("price") or 0)
        revenue = sold * price
        ticket_revenue += revenue
        occupancy = (sold / capacity * 100) if capacity else 0.0
        occupancy_samples.append(occupancy)
        by_festival[name] = {
            "capacity": int(capacity),
            "tickets_sold": int(sold),
            "occupancy": round(occupancy, 2),
            "revenue": round(revenue, 2),
        }

    by_role: Dict[str, int] = {}
    for user in users:
        role = str(user.get("role") or "cliente").lower()
        by_role[role] = by_role.get(role, 0) + 1

    return {
        "period_days": days,
        "summary": {
            "active_festivals": len(events),
            "registered_users": len(users),
            "orders": len(orders),
            "ticket_revenue": round(ticket_revenue, 2),
            "merch_revenue": merch_revenue,
            "total_revenue": round(ticket_revenue + merch_revenue, 2),
            "average_occupancy": round(sum(occupancy_samples) / len(occupancy_samples), 2) if occupancy_samples else 0.0,
        },
        "by_role": by_role,
        "by_festival": by_festival,
    }


def global_metrics_csv(days: int = 30) -> str:
    data = global_metrics(days)
    summary = data["summary"]
    lines = [
        "metrica,valor",
        f"festivales_activos,{summary['active_festivals']}",
        f"usuarios_registrados,{summary['registered_users']}",
        f"pedidos,{summary['orders']}",
        f"ingresos_entradas,{summary['ticket_revenue']}",
        f"ingresos_merchandising,{summary['merch_revenue']}",
        f"ingresos_totales,{summary['total_revenue']}",
        f"ocupacion_media,{summary['average_occupancy']}",
        "",
        "festival,aforo,entradas_vendidas,ocupacion,ingresos",
    ]
    for name, item in data["by_festival"].items():
        lines.append(f"{name},{item['capacity']},{item['tickets_sold']},{item['occupancy']},{item['revenue']}")
    return "\n".join(lines)
