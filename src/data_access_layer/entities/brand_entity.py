from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.data_access_layer.db_constants import BRAND_TBL_NAME
from src.data_access_layer.entities.base_entity import BaseEntity
from src.data_access_layer.entities.product_entity import Product


class BrandEntity(BaseEntity):

    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    image: str = Column(type_=String(length=120), nullable=False)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)
    products: list[Product] = relationship('ProductModel', backref='brand')
