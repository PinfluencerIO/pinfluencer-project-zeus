class BaseRepository:
    def __init__(self, data_manager, resource):
        self.__data_manager = data_manager
        self.__resource = resource

    def load_item(self):
        return self.__data_manager.session.query(self.__resource).first()

    def load_collection(self):
        return self.__data_manager.session.query(self.__resource).all()

    def load_by_id(self, id_):
        return self.__data_manager.session.query(self.__resource).filter(self.__resource.id == id_).first()


class BrandRepository(BaseRepository):
    def __init__(self, data_manager, resource):
        super().__init__(data_manager, resource)