from dataclasses import dataclass

from src.domain.models import brand_model
from src.domain.models.base_model import BaseModel


@dataclass
class ProductModel(BaseModel):
    name: str
    description: str
    requirements: str

