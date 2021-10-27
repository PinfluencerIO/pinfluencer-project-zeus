from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.brand_model import BrandModel


class BrandRepository:

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def get(self, id: str) -> BrandModel:
        result = self.__data_manager.session.query(BrandModel).filter(BrandModel.id == id).first()
        return result

    def get_all(self) -> list[BrandModel]:
        result = self.__data_manager.session.query(BrandModel).all()
        return result

    def create(self, data: BrandModel) -> bool:
        self.__data_manager.session.add(data)
        self.__data_manager.session.commit()
        # TODO: implement logic
        return True

    def update(self, id: str, data: BrandModel) -> bool:
        raise NotImplemented
