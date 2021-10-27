from src.domain.models.brand_model import BrandModel


class ProductModel:
    name: str
    description: str
    requirements: str
    image: str
    brand: BrandModel
