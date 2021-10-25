from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.product_model import ProductModel


class BrandRepository:

    __session_maker: DataManager

    def __init__(self, session_manager: DataManager):
        self.__session_maker = session_manager

    def get(self, id: str) -> ProductModel:
        return self.__session_maker.session.query(ProductModel).filter(ProductModel.id == id)

    def get_all(self) -> list[ProductModel]:
        return self.__session_maker.session.query(ProductModel)

    def create(self, data: ProductModel) -> ProductModel:
        return self.__session_maker.session.add(data)

    def update(self, id: str, data: ProductModel) -> bool:
        raise NotImplemented
