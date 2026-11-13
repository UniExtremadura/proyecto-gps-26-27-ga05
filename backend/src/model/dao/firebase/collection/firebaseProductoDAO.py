from ....dao.interfaceProductoDAO import InterfaceProductoDAO
from ....dto.productDTO import productDTO
from typing import List, Optional, Dict, Any

class FirebaseProductoDAO(InterfaceProductoDAO):

    def __init__(self, connector: Any) -> None:
        # conector compartido para operaciones firestore
        self.connector = connector
    
    def get_all_productos(self) -> List[Any]:
        try:
            # obtiene datos crudos y los mapea a dto de producto
            productos_data = self.connector.get_all_productos()
            productos = []
            for prod_data in productos_data:
                producto = productDTO()
                producto.set_id(prod_data.get("id"))
                producto.set_name(prod_data.get("name", ""))
                producto.set_category(prod_data.get("category", ""))
                producto.set_price(prod_data.get("price", 0))
                producto.set_provider(prod_data.get("provider", ""))
                producto.set_material(prod_data.get("material", ""))
                producto.set_shipping(prod_data.get("shipping", ""))
                producto.set_description(prod_data.get("description", ""))
                producto.set_colors(prod_data.get("colors", []))
                producto.set_images(prod_data.get("images", []))
                producto.set_stock(prod_data.get("stock", 0))
                producto.set_min_stock(prod_data.get("min_stock", 5))
                producto.set_provider_uid(prod_data.get("provider_uid") or prod_data.get("owner_uid"))
                producto.owner_uid = prod_data.get("owner_uid")
                producto.owner_email = prod_data.get("owner_email")
                producto.set_status(prod_data.get("status", "activo"))
                productos.append(producto)
            return productos
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    def get_producto_by_id(self, product_id: str) -> Optional[Any]:
        try:
            # consulta documento por id y lo convierte a dto
            producto_doc = self.connector.get_producto_by_id(product_id)
            if producto_doc is not None:
                prod_data = producto_doc.to_dict()
                producto = productDTO()
                producto.set_id(producto_doc.id)
                producto.set_name(prod_data.get("name", ""))
                producto.set_category(prod_data.get("category", ""))
                producto.set_price(prod_data.get("price", 0))
                producto.set_provider(prod_data.get("provider", ""))
                producto.set_material(prod_data.get("material", ""))
                producto.set_shipping(prod_data.get("shipping", ""))
                producto.set_description(prod_data.get("description", ""))
                producto.set_colors(prod_data.get("colors", []))
                producto.set_images(prod_data.get("images", []))
                producto.set_stock(prod_data.get("stock", 0))
                producto.set_min_stock(prod_data.get("min_stock", 5))
                producto.set_provider_uid(prod_data.get("provider_uid") or prod_data.get("owner_uid"))
                producto.owner_uid = prod_data.get("owner_uid")
                producto.owner_email = prod_data.get("owner_email")
                producto.set_status(prod_data.get("status", "activo"))
                return producto
            else:
                return None
        except Exception as e:
            print(f"Error getting product by id: {e}")
            return None

    def get_productos_by_provider(self, provider_id: str) -> List[Any]:
        try:
            # filtra productos por proveedor y mapea resultado a dto
            productos_data = self.connector.get_productos_by_provider(provider_id)
            productos = []
            for prod_data in productos_data:
                producto = productDTO()
                producto.set_id(prod_data.get("id"))
                producto.set_name(prod_data.get("name", ""))
                producto.set_category(prod_data.get("category", ""))
                producto.set_price(prod_data.get("price", 0))
                producto.set_provider(prod_data.get("provider", ""))
                producto.set_material(prod_data.get("material", ""))
                producto.set_shipping(prod_data.get("shipping", ""))
                producto.set_description(prod_data.get("description", ""))
                producto.set_colors(prod_data.get("colors", []))
                producto.set_images(prod_data.get("images", []))
                producto.set_stock(prod_data.get("stock", 0))
                producto.set_min_stock(prod_data.get("min_stock", 5))
                producto.set_provider_uid(prod_data.get("provider_uid") or prod_data.get("owner_uid"))
                producto.owner_uid = prod_data.get("owner_uid")
                producto.owner_email = prod_data.get("owner_email")
                producto.set_status(prod_data.get("status", "activo"))
                productos.append(producto)
            return productos
        except Exception as e:
            print(f"Error getting products by provider: {e}")
            return []

    def create_producto(self, producto_data: Dict[str, Any]) -> bool:
        try:
            # delega insercion al conector y devuelve exito booleano
            ref = self.connector.create_producto(producto_data)
            if ref:
                return True
            return False
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

    def update_producto(self, product_id: str, producto_data: Dict[str, Any]) -> bool:
        try:
            # delega actualizacion al conector y normaliza respuesta a booleano
            result = self.connector.update_producto(product_id, producto_data)
            if result:
                return True
            return False
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_producto(self, product_id: str) -> bool:
        try:
            # delega eliminacion al conector y normaliza respuesta a booleano
            result = self.connector.delete_producto(product_id)
            if result:
                return True
            return False
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
