from typing import Protocol, Optional

from src.domain.models import Brand


class BrandRepository(Protocol):

    def load_collection(self) -> list[Brand]:
        ...

    def load_by_id(self, id_: str) -> Optional[Brand]:
        ...

    def update_for_auth_user(self, auth_user_id: str, payload: Brand) -> Brand:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: Brand) -> Brand:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> Optional[Brand]:
        ...


class Validatable(Protocol):

    def validate(self, payload: dict) -> None:
        ...


class DataManager(Protocol):

    @property
    def engine(self):
        ...

    @property
    def session(self):
        ...
