from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from src.data_access_layer import BaseEntity, BaseMeta, BRAND_TBL_NAME


class Brand(BaseMeta, BaseEntity):
    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    instahandle: str = Column(type_=String(length=30), nullable=True)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)

    def as_dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "name": self.name,
            "description": self.description,
            "website":  self.website,
            "email": self.email,
            "instahandle": self.instahandle,
            "auth_user_id": self.auth_user_id
        }
