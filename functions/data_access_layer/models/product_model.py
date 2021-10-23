from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from functions.data_access_layer.models.model_base import ModelBase


class ProductModel(ModelBase):

    __tablename__ = 'product'

    id = Column(UUID, primary_key=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    requirements = Column(String)
    brand_id = Column(String)
    created = Column(DateTime)