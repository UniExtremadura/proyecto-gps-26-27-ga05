"""Servicio de moderación de cuentas y eventos (TK-014-1)."""
from datetime import datetime
from typing import Any, Dict, List

from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory

SUSPENDED_USERS: Dict[str, Dict[str, Any]] = {}
EVENT_MODERATION: Dict[str, str] = {}


def _connector():
    try:
        return FirebaseDAOFactory().connector
    except Exception:
        return None


def list_users() -> List[Dict[str, Any]]:
    connector = _connector()
    users = []
    if connector and connector.get_usuarios_collection() is not None:
        try:
            for doc in connector.get_usuarios_collection().stream():
                data = doc.to_dict() or {}
                data["uid"] = data.get("uid") or doc.id
                users.append(data)
        except Exception as exc:
            print(f"No se pudieron listar usuarios: {exc}")
    for uid, data in SUSPENDED_USERS.items():
        if not any(user.get("uid") == uid for user in users):
            users.append(data)
    return users


def suspend_user(uid: str, reason: str = "") -> bool:
    payload = {
        "uid": uid,
        "suspended": True,
        "suspended_reason": reason or "Incumplimiento de las normas",
        "suspended_at": datetime.now().isoformat(),
        "token_invalid_after": datetime.now().isoformat(),
    }
    SUSPENDED_USERS[uid] = payload
    connector = _connector()
    if connector and connector.get_usuarios_collection() is not None:
        try:
            connector.get_usuarios_collection().document(uid).update(payload)
        except Exception as exc:
            print(f"No se pudo suspender en Firestore: {exc}")
    return True


def reactivate_user(uid: str) -> bool:
    payload = {"suspended": False, "reactivated_at": datetime.now().isoformat()}
    SUSPENDED_USERS.pop(uid, None)
    connector = _connector()
    if connector and connector.get_usuarios_collection() is not None:
        try:
            connector.get_usuarios_collection().document(uid).update(payload)
        except Exception as exc:
            print(f"No se pudo reactivar en Firestore: {exc}")
    return True


def moderate_event(event_id: str, decision: str, reason: str = "") -> bool:
    normalized = str(decision or "").strip().lower()
    if normalized not in {"aprobado", "rechazado", "archivado"}:
        raise ValueError("Decisión de moderación no válida")
    EVENT_MODERATION[event_id] = normalized
    connector = _connector()
    if connector and connector.get_db():
        try:
            connector.get_db().collection("eventos").document(event_id).update(
                {
                    "moderation_status": normalized,
                    "moderation_reason": reason,
                    "moderated_at": datetime.now().isoformat(),
                }
            )
        except Exception as exc:
            print(f"No se pudo moderar el evento en Firestore: {exc}")
    return True
