from src.data_access_layer.entities import BrandEntity
from src.data_access_layer.write_data_access import AlreadyExistsException


class BaseRepository:
    def __init__(self, data_manager, resource):
        self._data_manager = data_manager
        self._resource = resource

    def load_item(self):
        return self._data_manager.session.query(self._resource).first()

    def load_collection(self):
        return self._data_manager.session.query(self._resource).all()

    def load_by_id(self, id_):
        return self._data_manager.session.query(self._resource).filter(self._resource.id == id_).first()


class BaseUserRepository(BaseRepository):
    def __init__(self, data_manager, resource):
        super().__init__(data_manager, resource)

    def load_for_auth_user(self, auth_user_id):
        first = self._data_manager.session.query(self._resource).filter(self._resource.auth_user_id == auth_user_id).first()
        print(f'load_brand_for_authenticated_user: {first}')
        return first


class BrandRepository(BaseUserRepository):
    def __init__(self, data_manager, image_repository):
        super().__init__(data_manager, BrandEntity)
        self.__image_repository = image_repository

    def write_new_for_auth_user(self, auth_user_id, payload):
        brand = self.load_for_auth_user(auth_user_id)
        if brand:
            raise AlreadyExistsException(f'Brand {brand.id} already associated with {auth_user_id}')
        else:
            try:
                payload.auth_user_id = auth_user_id
                brand = BrandEntity.from_dto(payload)
                self._data_manager.session.add(brand)
                self._data_manager.session.commit()
                return brand
            except Exception as e:
                print(f'Failed to write_new_brand {e}')
                self._data_manager.session.rollback()
                raise e