import uuid
from abc import abstractmethod
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

PRODUCT_TBL_NAME = 'product'
BRAND_TBL_NAME = 'brand'

BaseMeta = declarative_base()


class BaseEntity:
    __tablename__: str

    id: str = Column(type_=String(length=36), primary_key=True, default=uuid.uuid4, nullable=False)
    created: datetime = Column(DateTime, nullable=False)

    @abstractmethod
    def as_dict(self):
        pass


def to_list(data: list[BaseEntity]) -> list[dict]:
    data_dict: list[dict] = []
    for data_item in data:
        data_dict.append(data_item.as_dict())
    return data_dict
