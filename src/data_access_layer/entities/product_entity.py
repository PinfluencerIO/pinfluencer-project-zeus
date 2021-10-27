import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from src.data_access_layer.db_constants import PRODUCT_TBL_NAME
from src.data_access_layer.entities.base_entity import BaseEntity


class Product(BaseEntity):

    __tablename__ = PRODUCT_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    requirements: str = Column(type_=String(length=500), nullable=False)
    image: str = Column(type_=String(length=120), nullable=False)
    brand = relationship("BrandModel", back_populates="products")
