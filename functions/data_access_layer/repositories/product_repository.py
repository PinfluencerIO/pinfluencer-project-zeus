from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.product_model import ProductModel


class ProductRepository:

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def get(self, id: str) -> ProductModel:
        return self.__data_manager.session.query(ProductModel).filter(ProductModel.id == id)

    def get_all(self) -> list[ProductModel]:
        return self.__data_manager.session.query(ProductModel).all()

    def create(self, data: ProductModel) -> bool:
        self.__data_manager.session.add(data)
        self.__data_manager.session.commit()
        # TODO: add logic here
        return True

    def update(self, id: str, data: ProductModel) -> bool:
        raise NotImplemented

    def delete(self, id: str) -> bool:
        raise NotImplemented