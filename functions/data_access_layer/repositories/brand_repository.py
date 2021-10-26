from functions.data_access_layer.data_manager import DataManager
from functions.data_access_layer.models.brand_model import BrandModel


class BrandRepository:

    __session_maker: DataManager

    def __init__(self, session_manager: DataManager):
        self.__session_maker = session_manager

    def get(self, id: str) -> BrandModel:
        result = self.__session_maker.session.query(BrandModel).filter(BrandModel.id == id)
        self.__session_maker.session.commit()
        return result

    def get_all(self) -> list[BrandModel]:
        result = self.__session_maker.session.query(BrandModel)
        self.__session_maker.session.commit()
        return result

    def create(self, data: BrandModel) -> bool:
        self.__session_maker.session.add(data)
        self.__session_maker.session.commit()
        # TODO: implement logic
        return True

    def update(self, id: str, data: BrandModel) -> bool:
        raise NotImplemented
