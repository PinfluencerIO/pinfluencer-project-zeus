from src.domain.models.model_base import ModelBase
from src.domain.models.product_model import ProductModel


class BrandModel(ModelBase):
    name: str
    description: str
    website: str
    email: str
    image: str
    auth_user_id: str
    products: list[ProductModel]