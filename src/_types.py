from typing import Protocol, Optional, Union

from src.domain.models import Brand, Influencer, Campaign, User


class AuthUserRepository(Protocol):

    def update_brand_claims(self, user: User) -> None:
        ...

    def update_influencer_claims(self, user: User) -> None:
        ...

    def get_by_id(self, _id: str) -> User:
        ...


class CampaignRepository(Protocol):

    def load_collection(self) -> list[Campaign]:
        ...

    def load_by_id(self, id_: str) -> Campaign:
        ...

    def write_new_for_brand(self, payload: Campaign,
                            auth_user_id: str) -> Campaign:
        ...

    def load_for_auth_brand(self, auth_user_id: str) -> list[Campaign]:
        ...

    def save(self):
        ...


class BrandRepository(Protocol):

    def load_collection(self) -> list[Brand]:
        ...

    def load_by_id(self, id_: str) -> Brand:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: Brand) -> Brand:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> Brand:
        ...

    def save(self):
        ...


class InfluencerRepository(Protocol):

    def load_collection(self) -> list[Influencer]:
        ...

    def load_by_id(self, id_: str) -> Influencer:
        ...

    def load_for_auth_user(self, auth_user_id: str) -> Influencer:
        ...

    def write_new_for_auth_user(self, auth_user_id: str, payload: Influencer) -> Influencer:
        ...

    def save(self):
        ...


Repository = Union[BrandRepository,
                   InfluencerRepository,
                   CampaignRepository]

UserRepository = Union[BrandRepository, InfluencerRepository]


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


UserModel = Union[Brand, Influencer]

# TODO: add rest
Model = Union[UserModel, Campaign]


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


class Logger(Protocol):

    def log_error(self, message: str):
        ...

    def log_exception(self, exception: Exception):
        ...

    def log_info(self, message: str):
        ...

    def log_debug(self, message: str):
        ...

    def log_trace(self, message: str):
        ...
