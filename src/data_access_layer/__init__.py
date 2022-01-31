import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

PRODUCT_TBL_NAME = 'product'
BRAND_TBL_NAME = 'brand'


def uuid4_str():
    return str(uuid.uuid4())


@dataclass
class BaseEntity:
    id: str = Column(String(length=36), primary_key=True, default=uuid4_str, nullable=False)
    created: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "created": self.created
        }


Base = declarative_base()


def to_list(data):
    data_dict = []
    for data_item in data:
        data_dict.append(data_item.as_dict())
    return data_dict


class BaseUser(BaseEntity):
    first_name: str = Column(type_=String(length=120), nullable=False)
    last_name: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)

    def as_dict(self):
        dict = super().as_dict()
        dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "auth_user_id": self.auth_user_id
        })
        return dict
