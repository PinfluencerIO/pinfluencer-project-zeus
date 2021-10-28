from sqlalchemy.orm import Query

from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.product_entity import ProductEntity


class ProductRepository:

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def get(self, id: str) -> ProductEntity:
        query: Query = self.__data_manager.session.query(ProductEntity).filter(ProductEntity.id == id)
        return query.first()

    def get_all(self) -> list[ProductEntity]:
        return self.__data_manager.session.query(ProductEntity).all()

    def create(self, data: ProductEntity) -> bool:
        self.__data_manager.session.add(data)
        self.__data_manager.session.commit()
        # TODO: add logic here
        return True

    def update(self, id: str, data: ProductEntity) -> bool:
        raise NotImplemented

    def delete(self, id: str) -> bool:
        raise NotImplemented