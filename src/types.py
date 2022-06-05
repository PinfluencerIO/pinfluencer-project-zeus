from typing import Protocol, Optional, Union

from src.domain.models import Brand, Influencer, User


class UserRepository(Protocol):

    def load_collection(self) -> list[User]:
        ...

    def load_by_id(self, id_: str) -> User:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: User) -> User:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> User:
        ...


class BrandRepository(Protocol):

    def load_collection(self) -> list[Brand]:
        ...

    def load_by_id(self, id_: str) -> Brand:
        ...

    def update_for_auth_user(self, auth_user_id: str, payload: Brand) -> Brand:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: Brand) -> Brand:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> Brand:
        ...

    def update_logo_for_auth_user(self, auth_user_id: str, image_bytes: str) -> Brand:
        ...

    def update_header_image_for_auth_user(self, auth_user_id: str, image_bytes: str) -> Brand:
        ...


class InfluencerRepository(Protocol):

    def load_collection(self) -> list[Influencer]:
        ...

    def load_by_id(self, id_: str) -> Influencer:
        ...

    def update_for_auth_user(self, auth_user_id: str, payload: Influencer) -> Influencer:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: Influencer) -> Influencer:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> Influencer:
        ...

    def update_image_for_auth_user(self, auth_user_id: str, image_bytes: str) -> Influencer:
        ...


class InfluencerValidatable(Protocol):

    def validate_influencer(self, payload: dict) -> None:
        ...


class BrandValidatable(Protocol):

    def validate_brand(self, payload: dict) -> None:
        ...


class Queryable(Protocol):

    def filter(self, filter) -> 'Queryable':
        ...

    def first(self) -> Optional:
        ...

    def all(self) -> Optional[list]:
        ...


class SessionAdapter(Protocol):

    def query(self, entity) -> Queryable:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def add(self, entity) -> None:
        ...

    def flush(self) -> None:
        ...


class DataManager(Protocol):

    @property
    def engine(self):
        ...

    @property
    def session(self) -> SessionAdapter:
        ...


class ImageRepository(Protocol):

    def upload(self, path: str, image_base64_encoded: str) -> str:
        pass


User = Union[Brand, Influencer]

# TODO: add rest
Model = Union[User]


class ObjectMapperAdapter(Protocol):

    def create_map(self,
                   type_from: type,
                   type_to: type,
                   mapping: dict = None) -> None:
        pass

    def map(self,
            from_obj,
            to_type: type,
            ignore_case=False,
            allow_none=False,
            excluded=None):
        pass


class Serializer(Protocol):

    def serialize(self, data: Union[dict, list]) -> str:
        ...


class Deserializer(Protocol):

    def deserialize(self, data: str) -> Union[dict, list]:
        ...
