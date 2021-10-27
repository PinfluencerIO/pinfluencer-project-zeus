from sqlalchemy.orm import Query

from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.product_entity import Product


class ProductRepository:

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def get(self, id: str) -> Product:
        query: Query = self.__data_manager.session.query(Product).filter(Product.id == id)
        return query.first()

    def get_all(self) -> list[Product]:
        return self.__data_manager.session.query(Product).all()

    def create(self, data: Product) -> bool:
        self.__data_manager.session.add(data)
        self.__data_manager.session.commit()
        # TODO: add logic here
        return True

    def update(self, id: str, data: Product) -> bool:
        raise NotImplemented

    def delete(self, id: str) -> bool:
        raise NotImplemented