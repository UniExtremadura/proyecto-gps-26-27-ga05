"""Conector de base de datos local (MongoDB).

El proyecto se diseñó originalmente sobre Firebase/Firestore. Para poder
ejecutarlo completamente en local se mantiene la misma interfaz que usaba
``FirebaseConnector`` pero la persistencia se realiza en un contenedor de
MongoDB levantado con ``docker compose``.

La clase ``LocalDB`` implementa el pequeño subconjunto de la API de Firestore
que consumen los servicios y DAOs (``collection``, ``document``, ``stream``,
``where``, ``limit``, ``add``...). De esta forma el resto del código no necesita
saber qué motor hay debajo.
"""
from __future__ import annotations

import os
import threading
import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError

DB_NOT_INITIALIZED_MSG = "Database connection is not initialized."

_CLIENT_LOCK = threading.Lock()
_CLIENT: Optional[MongoClient] = None


def _new_id() -> str:
    return uuid.uuid4().hex


class LocalDocumentSnapshot:
    """Documento leído de MongoDB con la forma de un snapshot de Firestore."""

    def __init__(self, db: "LocalDB", collection: str, raw: Optional[Dict[str, Any]]) -> None:
        self._db = db
        self._collection = collection
        self._raw = raw
        self.exists = raw is not None
        self.id = str(raw.get("_id")) if raw else ""
        self.reference = LocalDocumentReference(db, collection, self.id)

    def to_dict(self) -> Dict[str, Any]:
        if not self._raw:
            return {}
        return {key: value for key, value in self._raw.items() if key != "_id"}


class LocalDocumentReference:
    def __init__(self, db: "LocalDB", collection: str, document_id: str) -> None:
        self._db = db
        self._collection = collection
        self.id = str(document_id)

    def get(self) -> LocalDocumentSnapshot:
        raw = self._db.raw_collection(self._collection).find_one({"_id": self.id})
        return LocalDocumentSnapshot(self._db, self._collection, raw)

    def set(self, data: Dict[str, Any], merge: bool = False) -> "LocalDocumentReference":
        payload = dict(data or {})
        payload.pop("_id", None)
        if merge:
            self._db.raw_collection(self._collection).update_one(
                {"_id": self.id}, {"$set": payload}, upsert=True
            )
        else:
            self._db.raw_collection(self._collection).replace_one(
                {"_id": self.id}, {"_id": self.id, **payload}, upsert=True
            )
        return self

    def update(self, data: Dict[str, Any]) -> None:
        payload = dict(data or {})
        payload.pop("_id", None)
        result = self._db.raw_collection(self._collection).update_one(
            {"_id": self.id}, {"$set": payload}
        )
        if result.matched_count == 0:
            raise LookupError(f"Documento no encontrado: {self._collection}/{self.id}")

    def delete(self) -> None:
        self._db.raw_collection(self._collection).delete_one({"_id": self.id})


class LocalQuery:
    def __init__(
        self,
        db: "LocalDB",
        collection: str,
        filters: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
    ) -> None:
        self._db = db
        self._collection = collection
        self._filters = list(filters or [])
        self._limit = limit

    def where(self, field: str, operator: str, value: Any) -> "LocalQuery":
        return LocalQuery(self._db, self._collection, self._filters + [(field, operator, value)], self._limit)

    def limit(self, value: int) -> "LocalQuery":
        return LocalQuery(self._db, self._collection, self._filters, int(value))

    def _mongo_filter(self) -> Dict[str, Any]:
        ops = {
            "==": "$eq",
            "!=": "$ne",
            "<": "$lt",
            "<=": "$lte",
            ">": "$gt",
            ">=": "$gte",
            "in": "$in",
            "not-in": "$nin",
        }
        query: Dict[str, Any] = {}
        for field, operator, value in self._filters:
            mongo_op = ops.get(operator)
            if mongo_op is None:
                raise ValueError(f"Operador no soportado: {operator}")
            if mongo_op == "$eq":
                query[field] = value
            else:
                query.setdefault(field, {})[mongo_op] = value
        return query

    def stream(self) -> Iterable[LocalDocumentSnapshot]:
        cursor = self._db.raw_collection(self._collection).find(self._mongo_filter())
        if self._limit:
            cursor = cursor.limit(self._limit)
        for raw in cursor:
            yield LocalDocumentSnapshot(self._db, self._collection, raw)


class LocalCollection:
    def __init__(self, db: "LocalDB", name: str) -> None:
        self._db = db
        self.name = name

    def document(self, document_id: str) -> LocalDocumentReference:
        return LocalDocumentReference(self._db, self.name, str(document_id))

    def add(self, data: Dict[str, Any]) -> LocalDocumentReference:
        document_id = _new_id()
        self.document(document_id).set(data or {})
        return self.document(document_id)

    def where(self, field: str, operator: str, value: Any) -> LocalQuery:
        return LocalQuery(self._db, self.name).where(field, operator, value)

    def limit(self, value: int) -> LocalQuery:
        return LocalQuery(self._db, self.name).limit(value)

    def count(self) -> int:
        return int(self._db.raw_collection(self.name).count_documents({}))

    def delete_many(self, query: Optional[Dict[str, Any]] = None) -> int:
        return int(self._db.raw_collection(self.name).delete_many(query or {}).deleted_count)


# ``LocalCollection.stream`` se define fuera de la clase para devolver
# generadores reales (y que el IDE no confunda ``find()`` con una lista).
def _collection_stream(self: LocalCollection):
    for raw in self._db.raw_collection(self.name).find():
        yield LocalDocumentSnapshot(self._db, self.name, raw)


LocalCollection.stream = _collection_stream  # type: ignore[assignment]


class LocalBatch:
    def __init__(self, db: "LocalDB") -> None:
        self._db = db
        self._deletions: List[LocalDocumentReference] = []

    def delete(self, reference: LocalDocumentReference) -> None:
        self._deletions.append(reference)

    def commit(self) -> None:
        for reference in self._deletions:
            reference.delete()
        self._deletions.clear()


class LocalDB:
    """Adaptador mínimo con apariencia de cliente Firestore."""

    def __init__(self, client: MongoClient, db_name: str) -> None:
        self.client = client
        self.name = db_name

    def raw_collection(self, name: str):
        return self.client[self.name][name]

    def collection(self, name: str) -> LocalCollection:
        return LocalCollection(self, name)

    def batch(self) -> LocalBatch:
        return LocalBatch(self)


def _get_client(uri: str, timeout_ms: int) -> MongoClient:
    global _CLIENT
    with _CLIENT_LOCK:
        if _CLIENT is None:
            _CLIENT = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
        return _CLIENT


class FirebaseConnector:
    """Conector compatible con la API histórica, respaldado por MongoDB."""

    firebase_app_initializated = False

    def __init__(self) -> None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "subsonic")
        timeout_ms = int(os.getenv("MONGO_TIMEOUT_MS", 5000))
        try:
            client = _get_client(uri, timeout_ms)
            client.admin.command("ping")
            self.client = client
            self.db: Optional[LocalDB] = LocalDB(client, db_name)
            FirebaseConnector.firebase_app_initializated = True
        except PyMongoError as exc:
            self.db = None
            raise ConnectionError(
                f"No se pudo conectar con MongoDB en {uri}. "
                "Ejecuta 'docker compose up -d mongodb' antes de arrancar el backend."
            ) from exc

    # ------------------------------------------------------------------
    # Acceso genérico
    # ------------------------------------------------------------------
    def get_db(self) -> Optional[LocalDB]:
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
        return self.db

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def get_usuarios_collection(self) -> Optional[LocalCollection]:
        return self.db.collection("usuarios") if self.db else None

    def get_usuario_by_uid(self, uid: str) -> Optional[LocalDocumentSnapshot]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            return self.db.collection("usuarios").document(uid).get()
        except Exception as exc:
            print(f"Error fetching user with UID {uid}: {exc}")
            return None

    def get_usuario_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        normalized = str(email or "").strip().lower()
        try:
            docs = list(self.db.collection("usuarios").where("email", "==", normalized).limit(1).stream())
            if docs:
                data = docs[0].to_dict()
                data["uid"] = data.get("uid") or docs[0].id
                return data
        except Exception as exc:
            print(f"Error fetching user by email: {exc}")
        return None

    def create_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            payload = dict(user_data)
            payload.setdefault("uid", uid)
            self.db.collection("usuarios").document(uid).set(payload)
            return True
        except Exception as exc:
            print(f"Error creating user: {exc}")
            return False

    def update_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("usuarios").document(uid).update(user_data)
            return True
        except LookupError:
            # Permite crear el perfil si el documento no existía todavía.
            payload = dict(user_data)
            payload.setdefault("uid", uid)
            self.db.collection("usuarios").document(uid).set(payload)
            return True
        except Exception as exc:
            print(f"Error updating user: {exc}")
            return False

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def get_productos_collection(self) -> Optional[LocalCollection]:
        return self.db.collection("productos") if self.db else None

    def get_all_productos(self) -> List[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        return self._all_docs("productos")

    def get_productos_by_provider(self, provider_id: str) -> List[Dict[str, Any]]:
        if not self.db:
            return []
        result = []
        for doc in self.db.collection("productos").stream():
            data = doc.to_dict()
            data["id"] = data.get("id") or doc.id
            if str(data.get("provider_uid") or data.get("owner_uid") or "") == str(provider_id):
                result.append(data)
        return result

    def get_producto_by_id(self, product_id: str) -> Optional[LocalDocumentSnapshot]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            return self.db.collection("productos").document(product_id).get()
        except Exception as exc:
            print(f"Error fetching product: {exc}")
            return None

    def create_producto(self, product_data: Dict[str, Any]) -> Optional[LocalDocumentReference]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            payload = dict(product_data)
            explicit_id = payload.pop("id", None)
            if explicit_id:
                ref = self.db.collection("productos").document(str(explicit_id))
                ref.set(payload)
                return ref
            return self.db.collection("productos").add(payload)
        except Exception as exc:
            print(f"Error creating product: {exc}")
            return None

    def update_producto(self, product_id: str, product_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).update(product_data)
            return True
        except Exception as exc:
            print(f"Error updating product: {exc}")
            return False

    def delete_producto(self, product_id: str) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).delete()
            return True
        except Exception as exc:
            print(f"Error deleting product: {exc}")
            return False

    # ------------------------------------------------------------------
    # Pedidos
    # ------------------------------------------------------------------
    def get_pedidos_collection(self) -> Optional[LocalCollection]:
        return self.db.collection("pedidos") if self.db else None

    def get_all_pedidos(self) -> List[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        return self._all_docs("pedidos")

    def get_pedidos_by_uid(self, uid: str) -> List[Dict[str, Any]]:
        if not self.db:
            return []
        result = []
        for doc in self.db.collection("pedidos").where("uid", "==", uid).stream():
            data = doc.to_dict()
            data["id"] = data.get("id") or doc.id
            result.append(data)
        result.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
        return result

    def get_pedido_by_id(self, order_id: str) -> Optional[LocalDocumentSnapshot]:
        if not self.db:
            return None
        try:
            return self.db.collection("pedidos").document(order_id).get()
        except Exception as exc:
            print(f"Error fetching order: {exc}")
            return None

    def create_pedido(self, order_data: Dict[str, Any]) -> Optional[LocalDocumentReference]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            payload = dict(order_data)
            explicit_id = payload.pop("id", None)
            if explicit_id:
                ref = self.db.collection("pedidos").document(str(explicit_id))
                ref.set(payload)
                return ref
            return self.db.collection("pedidos").add(payload)
        except Exception as exc:
            print(f"Error creating order: {exc}")
            return None

    def update_pedido(self, order_id: str, order_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("pedidos").document(order_id).update(order_data)
            return True
        except Exception as exc:
            print(f"Error updating order: {exc}")
            return False

    def clear_all_pedidos(self) -> int:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return 0
        try:
            deleted = self.db.collection("pedidos").delete_many()
            print(f"Pedidos eliminados: {deleted}")
            return deleted
        except Exception as exc:
            print(f"Error clearing orders collection: {exc}")
            return 0

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def get_eventos_collection(self) -> Optional[LocalCollection]:
        return self.db.collection("eventos") if self.db else None

    def get_all_eventos(self) -> List[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        return self._all_docs("eventos")

    def get_evento_by_id(self, event_id: str) -> Optional[LocalDocumentSnapshot]:
        if not self.db:
            return None
        try:
            return self.db.collection("eventos").document(event_id).get()
        except Exception as exc:
            print(f"Error fetching event: {exc}")
            return None

    def create_evento(self, event_data: Dict[str, Any]) -> Optional[LocalDocumentReference]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            payload = dict(event_data)
            explicit_id = payload.pop("id", None)
            if explicit_id:
                ref = self.db.collection("eventos").document(str(explicit_id))
                ref.set(payload)
                return ref
            return self.db.collection("eventos").add(payload)
        except Exception as exc:
            print(f"Error creating event: {exc}")
            return None

    def update_evento(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("eventos").document(event_id).update(event_data)
            return True
        except Exception as exc:
            print(f"Error updating event: {exc}")
            return False

    def delete_evento(self, event_id: str) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("eventos").document(event_id).delete()
            return True
        except Exception as exc:
            print(f"Error deleting event: {exc}")
            return False

    # ------------------------------------------------------------------
    # Artistas
    # ------------------------------------------------------------------
    def get_artistas_collection(self) -> Optional[LocalCollection]:
        return self.db.collection("artistas") if self.db else None

    def get_all_artistas(self) -> List[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        result = []
        for doc in self.db.collection("artistas").stream():
            data = doc.to_dict()
            data["id"] = data.get("id") or doc.id
            data["slug"] = data.get("slug") or doc.id
            result.append(data)
        return result

    def get_artista_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("artistas").document(slug).get()
            if doc.exists:
                data = doc.to_dict()
                data["id"] = data.get("id") or doc.id
                data["slug"] = data.get("slug") or slug
                return data
            docs = list(self.db.collection("artistas").where("slug", "==", slug).limit(1).stream())
            if docs:
                data = docs[0].to_dict()
                data["id"] = data.get("id") or docs[0].id
                data["slug"] = data.get("slug") or docs[0].id
                return data
        except Exception as exc:
            print(f"Error fetching artist by slug ({slug}): {exc}")
        return None

    def upsert_artista(self, slug: str, artist_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            payload = dict(artist_data)
            payload["slug"] = slug
            self.db.collection("artistas").document(slug).set(payload)
            return True
        except Exception as exc:
            print(f"Error upserting artist ({slug}): {exc}")
            return False

    def create_artista(self, artist_data: Dict[str, Any]) -> Optional[str]:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            payload = dict(artist_data)
            slug = payload.pop("slug", None) or payload.pop("id", None)
            if slug:
                payload["slug"] = str(slug)
                self.db.collection("artistas").document(str(slug)).set(payload)
                return str(slug)
            ref = self.db.collection("artistas").add(payload)
            return ref.id
        except Exception as exc:
            print(f"Error creating artist: {exc}")
            return None

    def get_artista_by_id(self, artist_id: str) -> Optional[LocalDocumentSnapshot]:
        if not self.db:
            return None
        try:
            return self.db.collection("artistas").document(artist_id).get()
        except Exception as exc:
            print(f"Error fetching artist by id ({artist_id}): {exc}")
            return None

    def update_artista(self, artist_id: str, artist_data: Dict[str, Any]) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("artistas").document(artist_id).update(artist_data)
            return True
        except Exception as exc:
            print(f"Error updating artist ({artist_id}): {exc}")
            return False

    def delete_artista(self, artist_id: str) -> bool:
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("artistas").document(artist_id).delete()
            return True
        except Exception as exc:
            print(f"Error deleting artist ({artist_id}): {exc}")
            return False

    def get_artista_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        if not self.db:
            return None
        normalized = str(name or "").strip().lower()
        try:
            for doc in self.db.collection("artistas").stream():
                data = doc.to_dict()
                if str(data.get("name", "")).strip().lower() == normalized:
                    data["id"] = data.get("id") or doc.id
                    data["slug"] = data.get("slug") or doc.id
                    return data
        except Exception as exc:
            print(f"Error fetching artist by name ({name}): {exc}")
        return None

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def update_producto_stock(self, product_id: str, stock: int, min_stock: int = 5) -> bool:
        """Actualiza stock y umbral de un producto (TK-010-1)."""
        if not self.db:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).update(
                {
                    "stock": int(stock),
                    "min_stock": int(min_stock),
                    "updated_at": datetime.now().isoformat(),
                }
            )
            return True
        except Exception as exc:
            print(f"Error updating product stock ({product_id}): {exc}")
            return False

    def _all_docs(self, collection: str) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for doc in self.db.collection(collection).stream():  # type: ignore[union-attr]
            data = doc.to_dict()
            data["id"] = data.get("id") or doc.id
            result.append(data)
        return result
