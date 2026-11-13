"""Datos de demostración para poder usar la aplicación desde el primer arranque.

Uso manual: ``python -m scripts.seed_demo``
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import get_connector
from model.roles import seed_roles
from security.password import hash_password

DEMO_USERS: List[Dict[str, Any]] = [
    {
        "uid": "local-cliente-demo",
        "email": "cliente.demo@subsonicfest.com",
        "name": "Cliente Demo",
        "role": "cliente",
        "password": "Cliente123!",
        "city": "Cáceres",
        "country": "España",
    },
    {
        "uid": "local-proveedor-demo",
        "email": "proveedor.demo@subsonicfest.com",
        "name": "Proveedor Demo",
        "role": "proveedor",
        "password": "Proveedor123!",
        "company_name": "Subsonic Merch SL",
        "business_area": "Merchandising",
        "city": "Badajoz",
        "country": "España",
    },
    {
        "uid": "local-gestor-demo",
        "email": "gestor.demo@subsonicfest.com",
        "name": "Gestor Demo",
        "role": "gestor",
        "password": "Gestor123!",
        "city": "Mérida",
        "country": "España",
    },
    {
        "uid": "local-admin-demo",
        "email": "admin.demo@subsonicfest.com",
        "name": "Admin Demo",
        "role": "admin",
        "password": "Admin123!",
        "city": "Madrid",
        "country": "España",
    },
]

DEMO_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "riverland-fest-2026",
        "name": "Riverland Fest 2026",
        "title": "Riverland Fest 2026",
        "genre": "indie",
        "location": "Pravia, Asturias",
        "loc": "Pravia, Asturias",
        "date": "2026-06-20",
        "ticket_price": 60,
        "available_tickets": 1200,
        "capacity": 5000,
        "tickets_sold": 3800,
        "image": "assets/img/riverland.svg",
        "description": "Festival de música y cultura en el corazón de Asturias.",
        "status": "publicado",
        "lineup": [
            {"name": "DJ Voltage", "role": "Headliner"},
            {"name": "Neon Shadow", "role": "Support"},
            {"name": "The Glitch", "role": "Special Guest"},
        ],
        "prices": {"general": 60, "vip": 150, "camping": 45},
    },
    {
        "id": "boombastic-costa-del-sol-2026",
        "name": "Boombastic Costa del Sol 2026",
        "title": "Boombastic Costa del Sol 2026",
        "genre": "urban",
        "location": "Torre del Mar, Málaga",
        "loc": "Torre del Mar, Málaga",
        "date": "2026-07-12",
        "ticket_price": 65,
        "available_tickets": 900,
        "capacity": 4000,
        "tickets_sold": 3100,
        "image": "assets/img/boombastic.svg",
        "description": "Festival de playa con el mejor ambiente del verano.",
        "status": "publicado",
        "lineup": [
            {"name": "Beach Pulse", "role": "Headliner"},
            {"name": "Solar Noise", "role": "Support"},
        ],
        "prices": {"general": 65, "vip": 160, "camping": 50},
    },
    {
        "id": "zevra-experience-2026",
        "name": "Zevra Experience 2026",
        "title": "Zevra Experience 2026",
        "genre": "electronic",
        "location": "Valencia",
        "loc": "Valencia",
        "date": "2026-08-01",
        "ticket_price": 55,
        "available_tickets": 700,
        "capacity": 3500,
        "tickets_sold": 2800,
        "image": "assets/img/zevra.svg",
        "description": "Una experiencia inmersiva de música electrónica.",
        "status": "publicado",
        "lineup": [
            {"name": "Neon Storm", "role": "Headliner"},
            {"name": "Acid Circuit", "role": "Support"},
        ],
        "prices": {"general": 55, "vip": 140, "camping": 40},
    },
]

DEMO_PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "camiseta-subsonic",
        "name": "Camiseta oficial Subsonic",
        "category": "Ropa",
        "price": 29.95,
        "provider": "Subsonic Merch SL",
        "provider_uid": "local-proveedor-demo",
        "owner_uid": "local-proveedor-demo",
        "owner_email": "proveedor.demo@subsonicfest.com",
        "material": "Algodón orgánico",
        "shipping": "3-5 días",
        "description": "Camiseta negra con logo luminoso del festival.",
        "colors": ["Negro", "Blanco"],
        "images": ["assets/img/camiseta.svg"],
        "stock": 42,
        "min_stock": 8,
        "status": "activo",
    },
    {
        "id": "gorra-subsonic",
        "name": "Gorra Subsonic",
        "category": "Accesorios",
        "price": 19.5,
        "provider": "Subsonic Merch SL",
        "provider_uid": "local-proveedor-demo",
        "owner_uid": "local-proveedor-demo",
        "owner_email": "proveedor.demo@subsonicfest.com",
        "material": "Poliéster",
        "shipping": "3-5 días",
        "description": "Gorra ajustable con bordado del festival.",
        "colors": ["Negro"],
        "images": ["assets/img/gorra.svg"],
        "stock": 4,
        "min_stock": 5,
        "status": "activo",
    },
    {
        "id": "vaso-reutilizable",
        "name": "Vaso reutilizable edición limitada",
        "category": "Coleccionables",
        "price": 12,
        "provider": "Subsonic Merch SL",
        "provider_uid": "local-proveedor-demo",
        "owner_uid": "local-proveedor-demo",
        "owner_email": "proveedor.demo@subsonicfest.com",
        "material": "Tritan",
        "shipping": "3-5 días",
        "description": "Vaso oficial reutilizable para todos los festivales.",
        "colors": ["Azul", "Rosa"],
        "images": ["assets/img/vaso.svg"],
        "stock": 120,
        "min_stock": 10,
        "status": "activo",
    },
    {
        "id": "poster-coleccion",
        "name": "Póster colección 2026",
        "category": "Coleccionables",
        "price": 15,
        "provider": "Subsonic Merch SL",
        "provider_uid": "local-proveedor-demo",
        "owner_uid": "local-proveedor-demo",
        "owner_email": "proveedor.demo@subsonicfest.com",
        "material": "Papel mate 250g",
        "shipping": "3-5 días",
        "description": "Póster numerado de la edición 2026.",
        "colors": [],
        "images": ["assets/img/poster.svg"],
        "stock": 30,
        "min_stock": 5,
        "status": "activo",
    },
]

DEMO_ARTISTS: List[Dict[str, Any]] = [
    {
        "id": "dj-voltage",
        "slug": "dj-voltage",
        "name": "DJ Voltage",
        "genre": "Electronic",
        "country": "España",
        "bio": "Productor y DJ de referencia en la escena electrónica.",
        "image": "assets/img/artist.svg",
    },
    {
        "id": "neon-shadow",
        "slug": "neon-shadow",
        "name": "Neon Shadow",
        "genre": "Indie",
        "country": "Portugal",
        "bio": "Banda indie con un directo lleno de energía.",
        "image": "assets/img/artist.svg",
    },
    {
        "id": "beach-pulse",
        "slug": "beach-pulse",
        "name": "Beach Pulse",
        "genre": "Urban",
        "country": "España",
        "bio": "Sonidos urbanos con sabor mediterráneo.",
        "image": "assets/img/artist.svg",
    },
]


def _collection_empty(connector: Any, name: str) -> bool:
    return connector.get_db().collection(name).count() == 0


def seed_demo_data(force: bool = False) -> Dict[str, int]:
    """Crea usuarios, eventos, productos y artistas de demostración."""
    connector = get_connector()
    now = datetime.now().isoformat()
    created = {"usuarios": 0, "eventos": 0, "productos": 0, "artistas": 0, "pedidos": 0, "roles": 0}

    # Roles del sistema
    try:
        created["roles"] = seed_roles(connector)
    except Exception as exc:  # pragma: no cover - la app sigue funcionando sin roles
        print(f"No se pudieron sembrar los roles: {exc}")

    # Usuarios
    for demo in DEMO_USERS:
        existing = connector.get_usuario_by_email(demo["email"])
        if existing and not force:
            continue
        payload = {key: value for key, value in demo.items() if key != "password"}
        payload.update(
            {
                "password_hash": hash_password(demo["password"]),
                "suspended": False,
                "created_at": existing.get("created_at") if existing else now,
                "updated_at": now,
            }
        )
        connector.create_usuario(demo["uid"], payload)
        created["usuarios"] += 1

    # Eventos
    if force or _collection_empty(connector, "eventos"):
        for event in DEMO_EVENTS:
            payload = dict(event)
            payload["created_at"] = now
            payload["updated_at"] = now
            connector.create_evento(payload)
            created["eventos"] += 1

    # Productos
    if force or _collection_empty(connector, "productos"):
        for product in DEMO_PRODUCTS:
            payload = dict(product)
            payload["created_at"] = now
            payload["updated_at"] = now
            connector.create_producto(payload)
            created["productos"] += 1

    # Artistas
    if force or _collection_empty(connector, "artistas"):
        for artist in DEMO_ARTISTS:
            payload = dict(artist)
            payload["created_at"] = now
            payload["updated_at"] = now
            connector.create_artista(payload)
            created["artistas"] += 1

    # Pedido de ejemplo para que el perfil y las métricas tengan datos.
    if force or _collection_empty(connector, "pedidos"):
        order = {
            "id": "pedido-demo-001",
            "uid": "local-cliente-demo",
            "email": "cliente.demo@subsonicfest.com",
            "items": [
                {
                    "id": "riverland-fest-2026",
                    "name": "Entrada General: Riverland Fest 2026",
                    "type": "Entrada",
                    "category": "Entradas",
                    "price": 60,
                    "quantity": 2,
                    "event_id": "riverland-fest-2026",
                },
                {
                    "id": "camiseta-subsonic",
                    "name": "Camiseta oficial Subsonic",
                    "type": "Merch",
                    "category": "Ropa",
                    "price": 29.95,
                    "quantity": 1,
                },
            ],
            "total": 149.95,
            "status": "completado",
            "payment_method": "demo",
            "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "updated_at": now,
        }
        connector.create_pedido(order)
        created["pedidos"] += 1

    return created


def seed_if_empty() -> Dict[str, int]:
    """Siembra los datos solo si la base de datos está vacía."""
    try:
        return seed_demo_data(force=False)
    except ConnectionError as exc:
        print(f"[seed] {exc}")
        return {}


def main() -> None:
    result = seed_demo_data(force=True)
    print("Datos de demostración sembrados:", result)


if __name__ == "__main__":
    main()
