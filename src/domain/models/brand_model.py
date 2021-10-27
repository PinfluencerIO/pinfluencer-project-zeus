from src.domain.models.product_model import ProductModel


class BrandModel:
    name: str
    description: str
    website: str
    email: str
    image: str
    auth_user_id: str
    products: list[ProductModel]