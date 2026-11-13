import json

class productDTO():
    def __init__(self):
        # atributos del producto tal como se guardan y devuelven en la api
        self.id = None
        self.name = None
        self.category = None
        self.price = None
        self.provider = None
        self.material = None
        self.shipping = None
        self.description = None
        self.colors = []
        self.images = []
        self.stock = 0
        self.min_stock = 5
        self.provider_uid = None
        self.owner_uid = None
        self.owner_email = None
        self.status = "activo"
        self.created_at = None
        self.updated_at = None

    def is_Empty(self):
        # considera vacio un producto sin id, nombre y precio
        return self.id is None and self.name is None and self.price is None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_category(self):
        return self.category
    
    def set_category(self, category):
        self.category = category

    def get_price(self):
        return self.price
    
    def set_price(self, price):
        self.price = price

    def get_provider(self):
        return self.provider
    
    def set_provider(self, provider):
        self.provider = provider

    def get_material(self):
        return self.material
    
    def set_material(self, material):
        self.material = material

    def get_shipping(self):
        return self.shipping
    
    def set_shipping(self, shipping):
        self.shipping = shipping

    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description

    def get_colors(self):
        return self.colors
    
    def set_colors(self, colors):
        self.colors = colors

    def get_images(self):
        return self.images
    
    def set_images(self, images):
        self.images = images

    def get_stock(self):
        return self.stock

    def set_stock(self, stock):
        self.stock = stock

    def get_min_stock(self):
        return self.min_stock

    def set_min_stock(self, min_stock):
        self.min_stock = min_stock

    def get_provider_uid(self):
        return self.provider_uid

    def set_provider_uid(self, provider_uid):
        self.provider_uid = provider_uid

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def product_to_dict(self):
        # transforma el dto a un objeto plano serializable
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "provider": self.provider,
            "material": self.material,
            "shipping": self.shipping,
            "description": self.description,
            "colors": self.colors,
            "images": self.images,
            "stock": self.stock,
            "min_stock": self.min_stock,
            "provider_uid": self.provider_uid,
            "owner_uid": self.owner_uid,
            "owner_email": self.owner_email,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def product_to_json(self):
        # retorna el contenido del producto como json string
        return json.dumps(self.product_to_dict())
