import dataclasses
import json
from abc import ABC
from datetime import datetime


@dataclasses.dataclass
class BaseModel(ABC):
    id: str
    created: datetime

    def as_dict(self) -> dict:
        return ModelExtensions.as_dict(self)


class ModelExtensions:
    @staticmethod
    def list_to_json(models: list[BaseModel]) -> str:
        return json.dumps(list(map(ModelExtensions.as_dict, models)), indent=4)

    @staticmethod
    def as_dict(model: BaseModel) -> dict:
        return dataclasses.asdict(model)

    @staticmethod
    def list_to_dict(models: list[BaseModel]) -> list[dict]:
        return list(map(ModelExtensions.as_dict, models))


@dataclasses.dataclass
class Owner(BaseModel):
    name: str


@dataclasses.dataclass
class ProductModel(BaseModel):
    name: str
    description: str
    requirements: str
    brand: Owner


@dataclasses.dataclass
class BrandModel(BaseModel):
    name: str
    description: str
    website: str
    email: str
    auth_user_id: str
    products: list[ProductModel]