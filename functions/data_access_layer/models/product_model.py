import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from functions.data_access_layer.db_constants import PRODUCT_TBL_NAME, BRAND_TBL_NAME
from functions.data_access_layer.models.model_base import ModelBase


class ProductModel(ModelBase):

    __tablename__ = PRODUCT_TBL_NAME

    id: str = Column(type_=String(length=36), primary_key=True, default=uuid.uuid4, nullable=False)
    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    requirements: str = Column(type_=String(length=500), nullable=False)
    image: str = Column(type_=String(length=120), nullable=False)
    brand_id: str = Column(String(length=36), ForeignKey(f"{BRAND_TBL_NAME}.id"))
    created: datetime = Column(DateTime, default=datetime.now, nullable=False)
