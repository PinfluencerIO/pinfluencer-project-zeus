from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.brand_entity import BrandEntity


class BrandRepository:

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def get(self, id: str) -> BrandEntity:
        result = self.__data_manager.session.query(BrandEntity).filter(BrandEntity.id == id).first()
        return result

    def get_all(self) -> list[BrandEntity]:
        result = self.__data_manager.session.query(BrandEntity).all()
        return result

    def create(self, data: dict) -> bool:
        self.__data_manager.session.add(data)
        self.__data_manager.session.commit()
        # TODO: implement logic
        return True

    def update(self, id: str, data: BrandEntity) -> bool:
        raise NotImplemented
