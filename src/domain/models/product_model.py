from dataclasses import dataclass

from src.domain.models import brand_model
from src.domain.models.base_model import BaseModel
import src.domain.models.brand_model as brand_module


@dataclass
class Owner(BaseModel):
    name: str


@dataclass
class ProductModel(BaseModel):
    name: str
    description: str
    requirements: str
    brand: Owner

