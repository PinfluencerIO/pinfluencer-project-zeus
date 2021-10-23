import uuid

from functions.data_access_layer.models.product_model import Product
from functions.domain.model import Brand


class ProductRepository:
    def get(self, id_: uuid) -> Product:
        raise NotImplemented

    def get_all(self) -> list[Product]:
        raise NotImplemented

    def create(self, data: Product) -> Product:
        raise NotImplemented

    def update(self, id_: uuid, data: Product) -> bool:
        raise NotImplemented

    def delete(self, id_: uuid) -> bool:
        raise NotImplemented