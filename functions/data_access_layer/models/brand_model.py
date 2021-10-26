import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from functions.data_access_layer import Base
from functions.data_access_layer.db_constants import BRAND_TBL_NAME
from functions.data_access_layer.models.product_model import ProductModel


class BrandModel(Base):

    __tablename__ = BRAND_TBL_NAME

    id: str = Column(type_=String(length=36), primary_key=True, default=uuid.uuid4, nullable=False)
    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    image: str = Column(type_=String(length=120), nullable=False)
    auth_user_id: str = Column(type_=String(length=64), nullable=False)
    created: datetime = Column(DateTime, default=datetime.now, nullable=False)
    products: list[ProductModel] = relationship(type(ProductModel).__name__, backref=BRAND_TBL_NAME)
