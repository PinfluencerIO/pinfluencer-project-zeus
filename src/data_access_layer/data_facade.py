import dataclasses
import json

from dacite import from_dict
from sqlalchemy import func, select, true
from sqlalchemy.orm import Query

from src.data_access_layer.alchemy_encoder import new_alchemy_encoder
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.brand_entity import BrandEntity
from src.data_access_layer.entities.product_entity import ProductEntity
from src.data_access_layer.repositories.alchemy_brand_repository import AlchemyBrandRepository
from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository
from src.domain.models.base_model import BaseModel
from src.domain.models.model_extensions import ModelExtensions
from src.domain.models.product_model import ProductModel

data_manager = DataManager()
brand_repository = AlchemyBrandRepository(data_manager=data_manager)
product_repository = AlchemyProductRepository(data_manager=data_manager)
products = product_repository.feed()

print(ModelExtensions.list_to_json(products))
print("")
#BrandEntity.metadata.create_all(bind=data_manager.engine)
#ProductEntity.metadata.create_all(bind=data_manager.engine)
