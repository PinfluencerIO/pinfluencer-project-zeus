from src.domain.models.model_base import ModelBase


class ProductModel(ModelBase):
    name: str
    description: str
    requirements: str
    image: str
