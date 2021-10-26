from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.brand_model import BrandModel


class BrandRepository:

    __session_maker: DataManager

    def __init__(self, session_manager: DataManager):
        self.__session_maker = session_manager

    def get(self, id: str) -> BrandModel:
        return self.__session_maker.session.query(BrandModel).filter(BrandModel.id == id)

    def get_all(self) -> list[BrandModel]:
        return self.__session_maker.session.query(BrandModel)

    def create(self, data: BrandModel) -> BrandModel:
        return self.__session_maker.session.add(data)

    def update(self, id: str, data: BrandModel) -> bool:
        raise NotImplemented
