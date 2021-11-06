from dataclasses import dataclass

from sqlalchemy import String, Column

from src.data_access_layer import BaseEntity, BaseMeta, BRAND_TBL_NAME


@dataclass
class Brand(BaseMeta, BaseEntity):
    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    instahandle: str = Column(type_=String(length=30), nullable=True)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)

    def as_dict(self) -> dict:
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


def brand_from_dict(brand: dict) -> Brand:
    auth_user_id = ""
    if "auth_user_id" in brand:
        auth_user_id = brand["auth_user_id"]
    return Brand(name=brand["name"],
                 description=brand["description"],
                 website=brand["website"],
                 email=brand["email"],
                 instahandle=brand["instahandle"],
                 auth_user_id=auth_user_id)
