from dataclasses import dataclass

from src.domain.models.base_model import BaseModel
from src.domain.models.product_model import ProductModel


@dataclass
class BrandModel(BaseModel):
    name: str
    description: str
    website: str
    email: str
    auth_user_id: str
    products: list[ProductModel]
