from typing import Protocol, Optional, Union

from src.domain.models import Brand, Influencer


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


class Validatable(Protocol):

    def validate(self, payload: dict) -> None:
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


class ObjectMapperAdapter:

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
