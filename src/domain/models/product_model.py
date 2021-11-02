from dataclasses import dataclass

from src.domain.models.model_base import ModelBase


@dataclass
class ProductModel(ModelBase):
    name: str
    description: str
    requirements: str
    image: str
