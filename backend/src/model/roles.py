"""Definición y siembra del esquema de roles (TK-002-1)."""
from typing import Any, Dict, List

# Roles del sistema. "organizador" se mantiene como alias de "gestor"
# para no romper el frontend existente.
ROLE_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "visitante": {
        "label": "Visitante",
        "description": "Usuario sin sesión; solo accede a rutas públicas.",
        "permissions": ["catalog:read", "events:read"],
    },
    "cliente": {
        "label": "Cliente",
        "description": "Compra entradas y merchandising.",
        "permissions": ["catalog:read", "events:read", "orders:create", "profile:update"],
    },
    "proveedor": {
        "label": "Proveedor",
        "description": "Gestiona recintos, stock y ventas de merchandising.",
        "permissions": ["catalog:read", "products:manage", "stock:manage", "bookings:manage", "sales:read"],
    },
    "gestor": {
        "label": "Organizador",
        "description": "Publica festivales y gestiona artistas y entradas.",
        "permissions": ["catalog:read", "events:manage", "artists:manage", "metrics:read"],
    },
    "organizador": {
        "label": "Organizador",
        "description": "Alias de gestor.",
        "permissions": ["catalog:read", "events:manage", "artists:manage", "metrics:read"],
    },
    "admin": {
        "label": "Administrador",
        "description": "Administra usuarios, moderación y métricas globales.",
        "permissions": ["*"],
    },
}

DEFAULT_ROLE = "cliente"
ROLE_ALIASES = {"organizador": "gestor"}


def normalize_role(role: str) -> str:
    """Normaliza y valida un rol; devuelve el rol por defecto si no existe."""
    value = str(role or "").strip().lower()
    value = ROLE_ALIASES.get(value, value)
    return value if value in ROLE_DEFINITIONS else DEFAULT_ROLE


def role_permissions(role: str) -> List[str]:
    normalized = normalize_role(role)
    return list(ROLE_DEFINITIONS.get(normalized, {}).get("permissions", []))


def has_permission(role: str, permission: str) -> bool:
    permissions = role_permissions(role)
    return "*" in permissions or permission in permissions


def seed_roles(connector: Any) -> int:
    """Crea/actualiza la colección `roles` en Firestore."""
    collection = connector.get_db().collection("roles") if connector.get_db() else None
    if collection is None:
        return 0
    count = 0
    for name, definition in ROLE_DEFINITIONS.items():
        collection.document(name).set({"name": name, **definition})
        count += 1
    return count
