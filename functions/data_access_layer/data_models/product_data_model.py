from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from functions.data_access_layer.data_models.data_model_base import Base


class Product(Base):

    __tablename__ = 'product'

    id = Column(UUID, primary_key=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    requirements = Column(String)
    brand_id = Column(String)
    created = Column(DateTime)