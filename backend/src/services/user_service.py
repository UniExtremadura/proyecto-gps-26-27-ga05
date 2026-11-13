"""Operaciones de usuario sobre la base de datos local."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from model.dao.firebase.firebaseDAOFactory import get_connector


def public_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Elimina credenciales y datos internos antes de devolver un usuario."""
    return {key: value for key, value in (user or {}).items() if key not in {"password_hash", "_id"}}


def get_user(uid: str) -> Optional[Dict[str, Any]]:
    if not uid:
        return None
    doc = get_connector().get_usuario_by_uid(uid)
    if doc is None or not getattr(doc, "exists", False):
        return None
    data = doc.to_dict()
    data["uid"] = data.get("uid") or doc.id
    return data


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    return get_connector().get_usuario_by_email(email)


def email_exists(email: str) -> bool:
    return find_user_by_email(email) is not None


def create_user(uid: str, data: Dict[str, Any]) -> bool:
    payload = dict(data or {})
    payload["uid"] = uid
    payload.setdefault("created_at", datetime.now().isoformat())
    payload["updated_at"] = datetime.now().isoformat()
    return get_connector().create_usuario(uid, payload)


def update_user(uid: str, data: Dict[str, Any]) -> bool:
    payload = dict(data or {})
    payload["updated_at"] = datetime.now().isoformat()
    return get_connector().update_usuario(uid, payload)


def list_users() -> List[Dict[str, Any]]:
    from services.moderation_service import list_users as moderation_list_users

    return moderation_list_users()
