"""Endpoints principales consumidos por el frontend (productos, pedidos,
eventos, artistas y paneles de gestor/proveedor).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Tuple

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse

from config.config import ERROR_MESSAGES
from model.dao.firebase.firebaseDAOFactory import get_connector
from security.rbac import get_current_user, require_roles
from services import user_service

router = APIRouter(tags=["core"])


def _connector():
    return get_connector()


def _all_docs(collection: str) -> List[Dict[str, Any]]:
    result = []
    for doc in _connector().get_db().collection(collection).stream():
        data = doc.to_dict()
        data["id"] = data.get("id") or doc.id
        result.append(data)
    return result


def _ok(data: Any = None, **extra):
    content: Dict[str, Any] = {"status": "success"}
    if data is not None:
        content["data"] = data
    content.update(extra)
    return JSONResponse(status_code=200, content=content)


# ---------------------------------------------------------------------------
# Productos
# ---------------------------------------------------------------------------
@router.get("/api/products")
async def list_products():
    products = _all_docs("productos")
    return _ok(products)


@router.get("/api/products/{product_id}")
async def product_detail(product_id: str):
    doc = _connector().get_producto_by_id(product_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
    data = doc.to_dict()
    data["id"] = data.get("id") or doc.id
    return _ok(data)


@router.post("/api/products")
async def create_product(
    data: dict = Body(...),
    user: dict = Depends(require_roles("proveedor", "gestor", "organizador", "admin")),
):
    payload = dict(data or {})
    if not str(payload.get("name") or "").strip():
        raise HTTPException(status_code=400, detail="El nombre del producto es obligatorio")
    try:
        payload["price"] = float(payload.get("price") or 0)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Precio no válido")
    payload.setdefault("stock", 0)
    payload.setdefault("min_stock", 5)
    payload.setdefault("status", "activo")
    payload["provider_uid"] = user["uid"]
    payload["owner_uid"] = user["uid"]
    payload["provider"] = payload.get("provider") or payload.get("company_name") or user.get("email", "")
    payload["owner_email"] = user.get("email", "")
    payload["created_at"] = datetime.now().isoformat()
    payload["updated_at"] = payload["created_at"]

    ref = _connector().create_producto(payload)
    if not ref:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return JSONResponse(
        status_code=201,
        content={"status": "success", "message": "Producto creado", "data": {"id": ref.id}},
    )


def _can_manage_product(product: Dict[str, Any], user: Dict[str, Any]) -> bool:
    if user.get("role") == "admin" or user.get("role") == "gestor":
        return True
    candidates = {
        str(product.get("provider_uid") or "").lower(),
        str(product.get("owner_uid") or "").lower(),
        str(product.get("owner_email") or "").lower(),
    }
    return bool(user.get("uid", "").lower() in candidates or user.get("email", "").lower() in candidates)


@router.put("/api/products/{product_id}")
async def update_product(
    product_id: str,
    data: dict = Body(...),
    user: dict = Depends(require_roles("proveedor", "gestor", "organizador", "admin")),
):
    doc = _connector().get_producto_by_id(product_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
    current = doc.to_dict()
    if not _can_manage_product(current, user):
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
    payload = dict(data or {})
    payload.pop("id", None)
    payload["updated_at"] = datetime.now().isoformat()
    if not _connector().update_producto(product_id, payload):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Producto actualizado")


@router.delete("/api/products/{product_id}")
async def delete_product(
    product_id: str,
    user: dict = Depends(require_roles("proveedor", "gestor", "organizador", "admin")),
):
    doc = _connector().get_producto_by_id(product_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
    if not _can_manage_product(doc.to_dict(), user):
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
    if not _connector().delete_producto(product_id):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Producto eliminado")


# ---------------------------------------------------------------------------
# Pedidos
# ---------------------------------------------------------------------------
def _normalize_items(items: Any) -> List[Dict[str, Any]]:
    if isinstance(items, dict):
        items = list(items.values())
    if not isinstance(items, list):
        return []
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
    return normalized


@router.get("/api/orders")
@router.get("/api/orders/me")
async def my_orders(user: dict = Depends(get_current_user)):
    orders = _connector().get_pedidos_by_uid(user["uid"])
    return _ok(orders)


@router.get("/api/orders/{order_id}")
async def order_detail(order_id: str, user: dict = Depends(get_current_user)):
    doc = _connector().get_pedido_by_id(order_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    data = doc.to_dict()
    data["id"] = data.get("id") or doc.id
    if data.get("uid") != user["uid"] and user.get("role") not in {"admin", "gestor"}:
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
    return _ok(data)


@router.post("/api/orders")
async def create_order(data: dict = Body(...), user: dict = Depends(get_current_user)):
    items = _normalize_items(data.get("items"))
    if not items:
        raise HTTPException(status_code=400, detail="El pedido no contiene productos")
    total = data.get("total")
    if total is None:
        total = sum(
            float(item.get("price") or 0) * int(item.get("quantity") or item.get("qty") or 1)
            for item in items
        )
    payload = {
        "uid": user["uid"],
        "email": user.get("email", ""),
        "items": items,
        "total": round(float(total or 0), 2),
        "status": str(data.get("status") or "pendiente"),
        "payment_method": str(data.get("payment_method") or "demo"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    ref = _connector().create_pedido(payload)
    if not ref:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    payload["id"] = ref.id
    return JSONResponse(
        status_code=201,
        content={"status": "success", "message": "Pedido creado", "data": payload},
    )


@router.put("/api/orders/{order_id}")
async def update_order(order_id: str, data: dict = Body(...), user: dict = Depends(get_current_user)):
    doc = _connector().get_pedido_by_id(order_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    current = doc.to_dict()
    if current.get("uid") != user["uid"] and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
    payload = {key: value for key, value in (data or {}).items() if key != "id"}
    payload["updated_at"] = datetime.now().isoformat()
    if not _connector().update_pedido(order_id, payload):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Pedido actualizado")


# ---------------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------------
@router.get("/api/events")
async def list_events():
    events = _all_docs("eventos")
    events.sort(key=lambda item: str(item.get("date", "")))
    return _ok(events)


@router.get("/api/events/search")
async def search_events(q: str = Query("")):
    needle = q.strip().lower()
    events = _all_docs("eventos")
    if needle:
        events = [
            event
            for event in events
            if needle
            in " ".join(
                str(event.get(field, ""))
                for field in ("name", "title", "description", "location", "loc", "genre", "artist")
            ).lower()
        ]
    return _ok(events)


@router.get("/api/events/{event_id}")
async def event_detail(event_id: str):
    doc = _connector().get_evento_by_id(event_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    data = doc.to_dict()
    data["id"] = data.get("id") or doc.id
    return _ok(data)


def _validate_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    name = str(payload.get("name") or payload.get("title") or "").strip()
    date = str(payload.get("date") or "").strip()
    location = str(payload.get("location") or payload.get("loc") or "").strip()
    if not name or not date or not location:
        raise HTTPException(status_code=400, detail="Nombre, fecha y ubicación son obligatorios")
    payload.update(
        {
            "name": name,
            "title": payload.get("title") or name,
            "date": date,
            "location": location,
            "loc": location,
            "ticket_price": float(payload.get("ticket_price") or payload.get("price") or 0),
            "available_tickets": int(payload.get("available_tickets") or payload.get("stock") or 0),
            "status": payload.get("status") or "publicado",
            "updated_at": datetime.now().isoformat(),
        }
    )
    return payload


@router.post("/api/events")
async def create_event(
    data: dict = Body(...),
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    payload = _validate_event(dict(data or {}))
    payload["created_at"] = datetime.now().isoformat()
    payload["created_by"] = user["uid"]
    ref = _connector().create_evento(payload)
    if not ref:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return JSONResponse(
        status_code=201,
        content={"status": "success", "message": "Evento creado", "data": {"id": ref.id}},
    )


@router.put("/api/events/{event_id}")
async def update_event(
    event_id: str,
    data: dict = Body(...),
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    doc = _connector().get_evento_by_id(event_id)
    if doc is None or not getattr(doc, "exists", False):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    payload = _validate_event({**doc.to_dict(), **dict(data or {})})
    payload.pop("id", None)
    if not _connector().update_evento(event_id, payload):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Evento actualizado")


@router.delete("/api/events/{event_id}")
async def delete_event(
    event_id: str,
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    if not _connector().delete_evento(event_id):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Evento eliminado")


# ---------------------------------------------------------------------------
# Artistas
# ---------------------------------------------------------------------------
@router.get("/api/artists")
async def list_artists():
    return _ok(_connector().get_all_artistas())


@router.get("/api/artists/search")
async def search_artists(q: str = Query(""), genre: str = Query("")):
    needle = q.strip().lower()
    artists = _connector().get_all_artistas()
    if needle:
        artists = [
            artist
            for artist in artists
            if needle in f"{artist.get('name', '')} {artist.get('genre', '')}".lower()
        ]
    if genre:
        artists = [artist for artist in artists if genre.lower() in str(artist.get("genre", "")).lower()]
    return _ok(artists)


@router.get("/api/artists/{slug}")
async def artist_detail(slug: str):
    artist = _connector().get_artista_by_slug(slug)
    if not artist:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return _ok(artist)


@router.post("/api/artists")
async def create_artist(
    data: dict = Body(...),
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    payload = dict(data or {})
    if not str(payload.get("name") or "").strip():
        raise HTTPException(status_code=400, detail="El nombre del artista es obligatorio")
    created = _connector().create_artista(payload)
    if not created:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return JSONResponse(status_code=201, content={"status": "success", "message": "Artista creado", "data": {"id": created}})


@router.put("/api/artists/{artist_id}")
async def update_artist(
    artist_id: str,
    data: dict = Body(...),
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    payload = dict(data or {})
    payload.pop("id", None)
    if not _connector().update_artista(artist_id, payload):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Artista actualizado")


@router.delete("/api/artists/{artist_id}")
async def delete_artist(
    artist_id: str,
    user: dict = Depends(require_roles("gestor", "organizador", "admin")),
):
    if not _connector().delete_artista(artist_id):
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    return _ok(message="Artista eliminado")


# ---------------------------------------------------------------------------
# Paneles de gestión y ventas
# ---------------------------------------------------------------------------
def _parse_dt(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    text = str(value or "").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _numeric(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _is_ticket(item: Dict[str, Any]) -> bool:
    kind = str(item.get("type") or item.get("category") or "").lower()
    return "entrada" in kind or "ticket" in kind or bool(item.get("event_id"))


def _provider_item_matches(item: Dict[str, Any], provider: Dict[str, Any], products_by_id: Dict[str, Dict[str, Any]]) -> bool:
    product = products_by_id.get(str(item.get("id") or item.get("product_id") or ""))
    targets = {
        str(provider.get("uid") or "").lower(),
        str(provider.get("email") or "").lower(),
        str(provider.get("name") or "").lower(),
        str(provider.get("company_name") or "").lower(),
    }
    targets.discard("")
    if product:
        candidates = {
            str(product.get("provider_uid") or "").lower(),
            str(product.get("owner_uid") or "").lower(),
            str(product.get("owner_email") or "").lower(),
            str(product.get("provider") or "").lower(),
        }
        if candidates & targets:
            return True
    item_candidates = {
        str(item.get("provider_uid") or "").lower(),
        str(item.get("provider") or "").lower(),
    }
    return bool(item_candidates & targets)


@router.get("/api/provider/sales")
async def provider_sales(user: dict = Depends(require_roles("proveedor", "admin"))):
    products = {str(product["id"]): product for product in _all_docs("productos")}
    orders = _all_docs("pedidos")
    operations: List[Dict[str, Any]] = []
    total = 0.0
    units = 0
    product_units: Dict[str, int] = {}
    today = datetime.now().date()

    for order in orders:
        if str(order.get("status", "")).lower() == "cancelada":
            continue
        created = _parse_dt(order.get("created_at"))
        for item in _normalize_items(order.get("items")):
            if _is_ticket(item) or not _provider_item_matches(item, user, products):
                continue
            quantity = max(1, int(item.get("quantity") or item.get("qty") or 1))
            price = _numeric(item.get("price"))
            line_total = round(price * quantity, 2)
            name = str(item.get("name") or item.get("product_name") or "Producto")
            total += line_total
            units += quantity
            product_units[name] = product_units.get(name, 0) + quantity
            operations.append(
                {
                    "id": str(order.get("id") or ""),
                    "item": name,
                    "type": "Venta Producto",
                    "date": created.strftime("%d/%m/%Y") if created else "",
                    "created_at": order.get("created_at"),
                    "amount": line_total,
                    "status": order.get("status", "pendiente"),
                    "quantity": quantity,
                }
            )

    operations.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
    today_sales = sum(
        item["amount"]
        for item in operations
        if (_parse_dt(item.get("created_at")) or datetime.min).date() == today
    )
    top_product = max(product_units.items(), key=lambda pair: pair[1])[0] if product_units else "Ninguno"
    return _ok(
        {
            "operations": operations,
            "summary": {
                "total_balance": round(total, 2),
                "sales_today": round(today_sales, 2),
                "units_sold": units,
                "top_product": top_product,
            },
        }
    )


@router.get("/api/manager/dashboard")
async def manager_dashboard(user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    events = _all_docs("eventos")
    orders = _all_docs("pedidos")
    users = _all_docs("usuarios")
    now = datetime.now()
    ticket_units: Dict[str, int] = {}
    ticket_revenue: Dict[str, float] = {}
    total_units = 0
    total_revenue = 0.0
    monthly_revenue = 0.0

    for order in orders:
        if str(order.get("status", "")).lower() == "cancelada":
            continue
        created = _parse_dt(order.get("created_at"))
        is_current_month = bool(created and created.month == now.month and created.year == now.year)
        for item in _normalize_items(order.get("items")):
            if not _is_ticket(item):
                continue
            quantity = max(1, int(item.get("quantity") or item.get("qty") or 1))
            line_total = _numeric(item.get("price")) * quantity
            total_units += quantity
            total_revenue += line_total
            if is_current_month:
                monthly_revenue += line_total
            event_id = str(item.get("event_id") or item.get("id") or "")
            if event_id:
                ticket_units[event_id] = ticket_units.get(event_id, 0) + quantity
                ticket_revenue[event_id] = ticket_revenue.get(event_id, 0.0) + line_total

    festivals = []
    for event in events:
        event_id = str(event.get("id") or "")
        festivals.append(
            {
                "id": event_id,
                "name": event.get("name") or event.get("title") or "Festival",
                "location": event.get("location") or event.get("loc") or "",
                "date": event.get("date") or "",
                "status": event.get("status") or "publicado",
                "tickets_sold": ticket_units.get(event_id, 0),
                "ticket_revenue": round(ticket_revenue.get(event_id, 0.0), 2),
            }
        )
    festivals.sort(key=lambda item: item["tickets_sold"], reverse=True)
    summary = {
        "total_users": len(users),
        "active_providers": len([item for item in users if item.get("role") == "proveedor"]),
        "total_festivals": len(festivals),
        "total_tickets_sold": total_units,
        "total_revenue": round(total_revenue, 2),
        "monthly_revenue": round(monthly_revenue, 2),
    }
    return _ok({"festivals": festivals, "summary": summary})


# ---------------------------------------------------------------------------
# Alias de perfil usados por versiones anteriores del frontend
# ---------------------------------------------------------------------------
@router.get("/api/user/profile")
async def legacy_get_profile(user: dict = Depends(get_current_user)):
    from controller.routers.profile_routes import _get_user

    profile = _get_user(user["uid"])
    return JSONResponse(status_code=200, content={"status": "success", "user": profile})


@router.put("/api/user/profile")
async def legacy_update_profile(data: dict = Body(...), user: dict = Depends(get_current_user)):
    from controller.routers.profile_routes import update_profile

    return await update_profile(data=data, user=user)
