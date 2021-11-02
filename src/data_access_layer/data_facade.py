import json

from src.data_access_layer.alchemy_encoder import new_alchemy_encoder
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.brand_entity import BrandEntity
from src.data_access_layer.entities.product_entity import ProductEntity
from src.data_access_layer.repositories.alchemy_brand_repository import AlchemyBrandRepository
from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository
from src.domain.models.product_model import ProductModel

data_manager = DataManager()
brand_repository = AlchemyBrandRepository(data_manager=data_manager)
product_repository = AlchemyProductRepository(data_manager=data_manager)
BrandEntity.metadata.create_all(bind=data_manager.engine)
ProductEntity.metadata.create_all(bind=data_manager.engine)
