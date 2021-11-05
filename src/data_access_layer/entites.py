import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.data_access_layer.db_constants import PRODUCT_TBL_NAME, BRAND_TBL_NAME
BaseMeta = declarative_base()


class BaseEntity:

    __tablename__: str

    id: str = Column(type_=String(length=36), primary_key=True, default=uuid.uuid4, nullable=False)
    created: datetime = Column(DateTime, nullable=False)


class ProductEntity(BaseEntity, BaseMeta):

    __tablename__ = PRODUCT_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    requirements: str = Column(type_=String(length=500), nullable=False)
    brand_id: str = Column(String(length=36), ForeignKey(f"{BRAND_TBL_NAME}.id"))
    brand = relationship('BrandEntity', back_populates='products')

    @property
    def owner(self):
        brand_to_return: BrandEntity = self.brand
        return brand_to_return


class BrandEntity(BaseEntity, BaseMeta):

    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    instahandle: str = Column(type_=String(length=30), nullable=True)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)
    products: list[ProductEntity] = relationship('ProductEntity', back_populates='brand')