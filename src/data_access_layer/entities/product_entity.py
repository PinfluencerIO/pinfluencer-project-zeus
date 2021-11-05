from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.data_access_layer.db_constants import PRODUCT_TBL_NAME, BRAND_TBL_NAME
from src.data_access_layer.entities.base_entity import BaseEntity, BaseMeta
import src.data_access_layer.entities.brand_entity as brand_module


class ProductEntity(BaseEntity, BaseMeta):

    __tablename__ = PRODUCT_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    requirements: str = Column(type_=String(length=500), nullable=False)
    brand_id: str = Column(String(length=36), ForeignKey(f"{BRAND_TBL_NAME}.id"))
    brand = relationship('BrandEntity', back_populates='products')

    @property
    def owner(self):
        brand_to_return: brand_module.BrandEntity = self.brand
        return brand_to_return
