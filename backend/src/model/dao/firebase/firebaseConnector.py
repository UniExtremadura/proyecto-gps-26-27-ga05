from firebase_admin import credentials, firestore, initialize_app, auth
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_NOT_INITIALIZED_MSG = "Database connection is not initialized."

class FirebaseConnector():
    # evita reinicializar la app de firebase admin mas de una vez por proceso
    firebase_app_initializated = False
    
    def __init__(self) -> None:
        # referencia al cliente firestore; puede quedar en none si falla inicializacion
        self.db: Optional[Any] = None
        try:
            if not FirebaseConnector.firebase_app_initializated:
                # busca credentials.json en rutas comunes del proyecto
                possible_paths = [
                    os.path.join(os.path.dirname(__file__), "credentials.json"),  # Same directory
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", "credentials.json"),  # Backend root
                    os.path.join(os.path.dirname(__file__), "..", "..", "config", "credentials.json"),  # Config folder
                ]
                
                credentials_path = None
                for path in possible_paths:
                    # toma la primera ruta valida encontrada
                    if os.path.exists(path):
                        credentials_path = path
                        break
                
                if not credentials_path:
                    raise FileNotFoundError(
                        f"credentials.json not found in any location:\n" + 
                        "\n".join(f"  - {p}" for p in possible_paths) +
                        "\n\nPlease download your Firebase credentials JSON from Firebase Console " +
                        "and place it in: backend/credentials.json"
                    )
                
                self.credentials = credentials.Certificate(credentials_path)
                initialize_app(self.credentials)
                FirebaseConnector.firebase_app_initializated = True
                print("Connection to Firebase Firestore initialized successfully.")
            
            # crea el cliente firestore que usan los daos
            self.db = firestore.client()
        except Exception as e:
            print(f"Error connecting to Firebase: {e}")
            raise

    def get_db(self) -> Optional[Any]:
        # devuelve el cliente bruto de firestore para usos avanzados
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
        return self.db

    # Colecciones de usuarios
    def get_usuarios_collection(self) -> Optional[Any]:
        # acceso centralizado a la coleccion de usuarios
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        return self.db.collection("usuarios")
    
    def get_usuario_by_uid(self, uid: str) -> Optional[Any]:
        # obtiene el documento de usuario por uid exacto
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            print(f"Fetching user with UID: {uid}")
            user_doc = self.db.collection("usuarios").document(uid).get()
            if user_doc.exists:
                print(f"User found: {user_doc.to_dict()}")
                return user_doc
            else:
                print(f"No user found with UID: {uid}")
                return None
        except Exception as e:
            print(f"Error fetching user with UID: {uid}: {e}")
            return None

    def create_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        # crea o reemplaza completamente el documento de usuario
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("usuarios").document(uid).set(user_data)
            print(f"User created successfully: {uid}")
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def update_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        # actualiza solo los campos enviados en el documento existente
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("usuarios").document(uid).update(user_data)
            print(f"User updated successfully: {uid}")
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    # Colecciones de productos
    def get_productos_collection(self) -> Optional[Any]:
        # acceso centralizado a la coleccion de productos
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        return self.db.collection("productos")

    def get_all_productos(self) -> List[Any]:
        # recorre todos los documentos y anade id al payload
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        try:
            docs = self.db.collection("productos").stream()
            products = []
            for doc in docs:
                product_data = doc.to_dict()
                product_data['id'] = doc.id
                products.append(product_data)
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []

    def get_producto_by_id(self, product_id: str) -> Optional[Any]:
        # devuelve el documento firestore del producto solicitado
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("productos").document(product_id).get()
            if doc.exists:
                return doc
            else:
                print(f"No product found with ID: {product_id}")
                return None
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None

    def create_producto(self, product_data: Dict[str, Any]) -> Optional[Any]:
        # crea un documento de producto con id generado por firestore
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            ref = self.db.collection("productos").add(product_data)
            print("Product created successfully")
            return ref
        except Exception as e:
            print(f"Error creating product: {e}")
            return None

    def update_producto(self, product_id: str, product_data: Dict[str, Any]) -> bool:
        # actualiza campos de un producto existente
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).update(product_data)
            print(f"Product updated successfully: {product_id}")
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_producto(self, product_id: str) -> bool:
        # elimina un producto por id
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).delete()
            print(f"Product deleted successfully: {product_id}")
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    # Colecciones de pedidos
    def get_pedidos_collection(self) -> Optional[Any]:
        # acceso centralizado a la coleccion de pedidos
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        return self.db.collection("pedidos")

    def get_all_pedidos(self) -> List[Any]:
        # obtiene pedidos completos e incluye id del documento
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        try:
            docs = self.db.collection("pedidos").stream()
            orders = []
            for doc in docs:
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def get_pedidos_by_uid(self, uid: str) -> List[Any]:
        # filtra pedidos por uid para historial de un usuario concreto
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        try:
            docs = self.db.collection("pedidos").where("uid", "==", uid).stream()
            orders = []
            for doc in docs:
                order_data = doc.to_dict()
                order_data['id'] = doc.id
                orders.append(order_data)
            return orders
        except Exception as e:
            print(f"Error fetching orders for user: {e}")
            return []

    def get_pedido_by_id(self, order_id: str) -> Optional[Any]:
        # devuelve documento de pedido por id
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("pedidos").document(order_id).get()
            if doc.exists:
                return doc
            else:
                print(f"No order found with ID: {order_id}")
                return None
        except Exception as e:
            print(f"Error fetching order: {e}")
            return None

    def create_pedido(self, order_data: Dict[str, Any]) -> Optional[Any]:
        # inserta pedido nuevo en la coleccion de pedidos
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            ref = self.db.collection("pedidos").add(order_data)
            print("Order created successfully")
            return ref
        except Exception as e:
            print(f"Error creating order: {e}")
            return None

    def update_pedido(self, order_id: str, order_data: Dict[str, Any]) -> bool:
        # actualiza campos de un pedido existente
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("pedidos").document(order_id).update(order_data)
            print(f"Order updated successfully: {order_id}")
            return True
        except Exception as e:
            print(f"Error updating order: {e}")
            return False

    def clear_all_pedidos(self) -> int:
        """Elimina todos los pedidos de Firestore y devuelve el total eliminado."""
        # se usa como limpieza para entorno de demo y pruebas
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return 0

        try:
            collection = self.db.collection("pedidos")
            docs = list(collection.stream())
            if not docs:
                return 0

            deleted_count = 0
            batch = self.db.batch()
            ops_in_batch = 0

            for doc in docs:
                batch.delete(doc.reference)
                ops_in_batch += 1

                # Firestore permite hasta 500 operaciones por batch.
                if ops_in_batch == 450:
                    batch.commit()
                    deleted_count += ops_in_batch
                    batch = self.db.batch()
                    ops_in_batch = 0

            if ops_in_batch > 0:
                batch.commit()
                deleted_count += ops_in_batch

            print(f"Pedidos eliminados al cerrar backend: {deleted_count}")
            return deleted_count
        except Exception as e:
            print(f"Error clearing orders collection: {e}")
            return 0

    # Colecciones de eventos
    def get_eventos_collection(self) -> Optional[Any]:
        # acceso centralizado a la coleccion de eventos
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        return self.db.collection("eventos")

    def get_all_eventos(self) -> List[Any]:
        # obtiene todos los eventos con su id de documento
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        try:
            docs = self.db.collection("eventos").stream()
            events = []
            for doc in docs:
                event_data = doc.to_dict()
                event_data['id'] = doc.id
                events.append(event_data)
            return events
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []

    def get_evento_by_id(self, event_id: str) -> Optional[Any]:
        # devuelve documento de evento por id
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("eventos").document(event_id).get()
            if doc.exists:
                return doc
            else:
                print(f"No event found with ID: {event_id}")
                return None
        except Exception as e:
            print(f"Error fetching event: {e}")
            return None

    def create_evento(self, event_data: Dict[str, Any]) -> Optional[Any]:
        # inserta un evento nuevo con id automatico
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            ref = self.db.collection("eventos").add(event_data)
            print("Event created successfully")
            return ref
        except Exception as e:
            print(f"Error creating event: {e}")
            return None

    def update_evento(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        # aplica cambios sobre un evento existente
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("eventos").document(event_id).update(event_data)
            print(f"Event updated successfully: {event_id}")
            return True
        except Exception as e:
            print(f"Error updating event: {e}")
            return False

    def delete_evento(self, event_id: str) -> bool:
        # elimina un evento por id de documento
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("eventos").document(event_id).delete()
            print(f"Event deleted successfully: {event_id}")
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

    # Colecciones de artistas
    def get_artistas_collection(self) -> Optional[Any]:
        # acceso centralizado a la coleccion de artistas
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        return self.db.collection("artistas")

    def get_all_artistas(self) -> List[Dict[str, Any]]:
        # devuelve artistas en formato diccionario, garantizando campo slug
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return []
        try:
            docs = self.db.collection("artistas").stream()
            artistas = []
            for doc in docs:
                data = doc.to_dict() or {}
                data["slug"] = data.get("slug") or doc.id
                artistas.append(data)
            return artistas
        except Exception as e:
            print(f"Error fetching artists: {e}")
            return []

    def get_artista_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        # busca primero por id documento y luego por campo slug
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("artistas").document(slug).get()
            if doc.exists:
                data = doc.to_dict() or {}
                data["slug"] = data.get("slug") or slug
                return data

            docs = self.db.collection("artistas").where("slug", "==", slug).limit(1).stream()
            for match in docs:
                data = match.to_dict() or {}
                data["slug"] = data.get("slug") or match.id
                return data

            return None
        except Exception as e:
            print(f"Error fetching artist by slug ({slug}): {e}")
            return None

    def upsert_artista(self, slug: str, artist_data: Dict[str, Any]) -> bool:
        # crea o reemplaza el artista usando slug como clave estable
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            payload = dict(artist_data)
            payload["slug"] = slug
            self.db.collection("artistas").document(slug).set(payload)
            return True
        except Exception as e:
            print(f"Error upserting artist ({slug}): {e}")
            return False

    def create_artista(self, artist_data: Dict[str, Any]) -> Optional[str]:
        # crea artista por slug si existe, o con id autogenerado si no existe
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            # Usar slug como ID de documento si está disponible
            slug = artist_data.get("slug", None)
            if slug:
                self.db.collection("artistas").document(slug).set(artist_data)
                return slug
            else:
                # Si no hay slug, generar automáticamente un ID
                ref = self.db.collection("artistas").add(artist_data)
                return ref[1].id
        except Exception as e:
            print(f"Error creating artist: {e}")
            return None

    def get_artista_by_id(self, artist_id: str) -> Optional[Any]:
        # devuelve documento de artista por id exacto
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            doc = self.db.collection("artistas").document(artist_id).get()
            if doc.exists:
                return doc
            return None
        except Exception as e:
            print(f"Error fetching artist by id ({artist_id}): {e}")
            return None

    def update_artista(self, artist_id: str, artist_data: Dict[str, Any]) -> bool:
        # actualiza campos del artista indicado
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("artistas").document(artist_id).update(artist_data)
            return True
        except Exception as e:
            print(f"Error updating artist ({artist_id}): {e}")
            return False

    def delete_artista(self, artist_id: str) -> bool:
        # elimina el artista indicado
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("artistas").document(artist_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting artist ({artist_id}): {e}")
            return False

    def get_artista_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Buscar artista por nombre en Firestore"""
        # intenta igualdad exacta y luego comparacion normalizada
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return None
        try:
            # Normalizar nombre para búsqueda case-insensitive
            name_lower = name.lower().strip()
            
            # Buscar en campo 'name'
            docs = self.db.collection("artistas").where("name", "==", name).limit(1).stream()
            for doc in docs:
                data = doc.to_dict() or {}
                data["slug"] = data.get("slug") or doc.id
                return data
            
            # Si no encuentra exacto, buscar con búsqueda parcial (startswith)
            docs = self.db.collection("artistas").stream()
            for doc in docs:
                data = doc.to_dict() or {}
                artist_name = data.get("name", "").lower().strip()
                if artist_name == name_lower:
                    data["slug"] = data.get("slug") or doc.id
                    return data
            
            return None
        except Exception as e:
            print(f"Error fetching artist by name ({name}): {e}")
            return None

    def update_producto_stock(self, product_id: str, stock: int, min_stock: int = 5) -> bool:
        """Actualiza stock y umbral de un producto (TK-010-1)."""
        if self.db is None:
            print(DB_NOT_INITIALIZED_MSG)
            return False
        try:
            self.db.collection("productos").document(product_id).update(
                {"stock": int(stock), "min_stock": int(min_stock)}
            )
            return True
        except Exception as e:
            print(f"Error updating product stock ({product_id}): {e}")
            return False
