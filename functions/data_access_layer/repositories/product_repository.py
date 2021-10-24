import uuid

from sqlalchemy.dialects.postgresql import UUID

from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.product_model import ProductModel
from functions.domain.model import Brand


class ProductRepository:

    __session_maker: DataManager

    def __init__(self, session_manager: DataManager):
        self.__session_maker = session_manager

    def get(self, id: UUID) -> ProductModel:
        return self.__session_maker.session.get(ProductModel, ident=id)

    def get_all(self) -> list[ProductModel]:
        return self.__session_maker.session.get(ProductModel)

    def create(self, data: ProductModel) -> ProductModel:
        return self.__session_maker.session.add(data)

    def update(self, id: UUID, data: ProductModel) -> bool:
        raise NotImplemented

    def delete(self, id: UUID) -> bool:
        raise NotImplemented