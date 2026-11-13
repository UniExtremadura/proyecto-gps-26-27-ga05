from .factory.interfaceDAOFactory import InterfaceDAOFactory
import json
from datetime import datetime
from typing import Dict, Any, Optional

class Model():
    def __init__(self, factory: InterfaceDAOFactory):
        # guarda la factoria para obtener daos concretos segun implementacion
        self.factory = factory
        # referencias a daos que operan sobre cada dominio de datos
        self.usuario_dao = None
        self.pedido_dao = None
        self.producto_dao = None
        self.evento_dao = None
        try:
            # inicializa los daos compartidos que no dependen de uid de usuario
            self.pedido_dao = self.factory.getPedidosDAO()
            self.producto_dao = self.factory.getProductosDAO()
            self.evento_dao = self.factory.getEventosDAO()
        except Exception as e:
            print(f"Error initializing DAOs: {e}")
            raise
    
    # Métodos de Usuario
    def get_usuario(self, uid: str) -> Optional[Any]:
        try:
            # este dao se construye por uid para leer el perfil de usuario concreto
            usuario_dao = self.factory.getUsuarioDAO(uid)
            return usuario_dao.get_usuario(uid)
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def create_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        try:
            # usa el conector para persistir directamente el documento en firestore
            connector = self.factory.connector
            return connector.create_usuario(uid, user_data)
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def update_usuario(self, uid: str, user_data: Dict[str, Any]) -> bool:
        try:
            # actualiza campos parciales del usuario existente
            connector = self.factory.connector
            return connector.update_usuario(uid, user_data)
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    # Métodos de Pedidos
    def get_all_pedidos(self) -> str:
        try:
            # transforma dto a diccionario para serializar respuesta json
            pedidos = self.pedido_dao.get_all_pedidos()
            return json.dumps([p.order_to_dict() for p in pedidos])
        except Exception as e:
            print(f"Error getting all orders: {e}")
            return json.dumps([])
    
    def get_pedidos_by_uid(self, uid: str) -> str:
        try:
            pedidos = self.pedido_dao.get_pedidos_by_uid(uid)
            return json.dumps([p.order_to_dict() for p in pedidos])
        except Exception as e:
            print(f"Error getting orders for user: {e}")
            return json.dumps([])

    def get_pedido_by_id(self, order_id: str) -> str:
        try:
            pedido = self.pedido_dao.get_pedido_by_id(order_id)
            if pedido:
                return json.dumps(pedido.order_to_dict())
            return json.dumps({})
        except Exception as e:
            print(f"Error getting order: {e}")
            return json.dumps({})

    def create_pedido(self, order_data: Dict[str, Any]) -> bool:
        try:
            # agrega timestamps de creacion y actualizacion antes de guardar
            order_data['created_at'] = datetime.now().isoformat()
            order_data['updated_at'] = datetime.now().isoformat()
            return self.pedido_dao.create_pedido(order_data)
        except Exception as e:
            print(f"Error creating order: {e}")
            return False

    def update_pedido(self, order_id: str, order_data: Dict[str, Any]) -> bool:
        try:
            # mantiene la fecha de actualizacion sincronizada en cada cambio
            order_data['updated_at'] = datetime.now().isoformat()
            return self.pedido_dao.update_pedido(order_id, order_data)
        except Exception as e:
            print(f"Error updating order: {e}")
            return False

    def clear_all_pedidos(self) -> int:
        try:
            # limpieza util para reiniciar el historial de compras al apagar el backend
            connector = self.factory.connector
            return connector.clear_all_pedidos()
        except Exception as e:
            print(f"Error clearing all orders: {e}")
            return 0
    
    # Métodos de Productos
    def get_all_productos(self) -> str:
        try:
            # convierte cada dto de producto a estructura serializable
            productos = self.producto_dao.get_all_productos()
            return json.dumps([p.product_to_dict() for p in productos])
        except Exception as e:
            print(f"Error getting all products: {e}")
            return json.dumps([])

    def get_producto_by_id(self, product_id: str) -> str:
        try:
            producto = self.producto_dao.get_producto_by_id(product_id)
            if producto:
                return json.dumps(producto.product_to_dict())
            return json.dumps({})
        except Exception as e:
            print(f"Error getting product: {e}")
            return json.dumps({})

    def create_producto(self, product_data: Dict[str, Any]) -> bool:
        try:
            # inicializa metadatos de tiempo para auditoria basica
            product_data['created_at'] = datetime.now().isoformat()
            product_data['updated_at'] = datetime.now().isoformat()
            return self.producto_dao.create_producto(product_data)
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

    def update_producto(self, product_id: str, product_data: Dict[str, Any]) -> bool:
        try:
            # mantiene fecha de actualizacion en cada modificacion
            product_data['updated_at'] = datetime.now().isoformat()
            return self.producto_dao.update_producto(product_id, product_data)
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_producto(self, product_id: str) -> bool:
        try:
            return self.producto_dao.delete_producto(product_id)
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    # Métodos de Eventos
    def get_all_eventos(self) -> str:
        try:
            # empaqueta resultados de eventos en json para respuesta http
            eventos = self.evento_dao.get_all_eventos()
            return json.dumps([e.event_to_dict() for e in eventos])
        except Exception as e:
            print(f"Error getting all events: {e}")
            return json.dumps([])

    def get_evento_by_id(self, event_id: str) -> str:
        try:
            evento = self.evento_dao.get_evento_by_id(event_id)
            if evento:
                return json.dumps(evento.event_to_dict())
            return json.dumps({})
        except Exception as e:
            print(f"Error getting event: {e}")
            return json.dumps({})

    def create_evento(self, event_data: Dict[str, Any]) -> bool:
        try:
            # agrega fechas de control antes de insertar nuevo evento
            event_data['created_at'] = datetime.now().isoformat()
            event_data['updated_at'] = datetime.now().isoformat()
            return self.evento_dao.create_evento(event_data)
        except Exception as e:
            print(f"Error creating event: {e}")
            return False

    def update_evento(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        try:
            # actualiza timestamp para reflejar modificacion del evento
            event_data['updated_at'] = datetime.now().isoformat()
            return self.evento_dao.update_evento(event_id, event_data)
        except Exception as e:
            print(f"Error updating event: {e}")
            return False

    def delete_evento(self, event_id: str) -> bool:
        try:
            return self.evento_dao.delete_evento(event_id)
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

    # Metodos de Artistas
    def get_all_artistas(self) -> str:
        try:
            # usa el conector porque el formato de artistas se consume como lista plana
            artistas = self.factory.connector.get_all_artistas()
            return json.dumps(artistas)
        except Exception as e:
            print(f"Error getting all artists: {e}")
            return json.dumps([])

    def get_artista_by_slug(self, slug: str) -> str:
        try:
            artista = self.factory.connector.get_artista_by_slug(slug)
            return json.dumps(artista or {})
        except Exception as e:
            print(f"Error getting artist by slug: {e}")
            return json.dumps({})

    def get_artista_by_id(self, artist_id: str) -> str:
        try:
            # obtiene dto y lo serializa a json normalizado para el frontend
            artista_dao = self.factory.getArtistasDAO()
            artista = artista_dao.get_artista_by_id(artist_id)
            if artista:
                artista_json = json.loads(artista.to_json())
                return json.dumps(artista_json)
            return json.dumps({})
        except Exception as e:
            print(f"Error getting artist by id: {e}")
            return json.dumps({})

    def create_artista(self, artist_data: dict) -> bool:
        try:
            # delega creacion al dao especifico de artistas
            artista_dao = self.factory.getArtistasDAO()
            return artista_dao.create_artista(artist_data)
        except Exception as e:
            print(f"Error creating artist: {e}")
            return False

    def update_artista(self, artist_id: str, artist_data: dict) -> bool:
        try:
            artista_dao = self.factory.getArtistasDAO()
            return artista_dao.update_artista(artist_id, artist_data)
        except Exception as e:
            print(f"Error updating artist: {e}")
            return False

    def delete_artista(self, artist_id: str) -> bool:
        try:
            artista_dao = self.factory.getArtistasDAO()
            return artista_dao.delete_artista(artist_id)
        except Exception as e:
            print(f"Error deleting artist: {e}")
            return False
    
    def update_producto_stock(self, product_id: str, stock: int, min_stock: int = 5) -> bool:
        """Actualiza el stock de un producto (TK-010-1)."""
        try:
            return self.factory.connector.update_producto_stock(product_id, stock, min_stock)
        except Exception as e:
            print(f"Error updating product stock: {e}")
            return False
