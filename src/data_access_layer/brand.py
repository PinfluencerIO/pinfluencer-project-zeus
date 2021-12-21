from dataclasses import dataclass

from sqlalchemy import String, Column

from src.data_access_layer import Base, BRAND_TBL_NAME, BaseEntity


@dataclass
class Brand(Base, BaseEntity):
    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    website: str = Column(type_=String(length=120), nullable=False)
    email: str = Column(type_=String(length=120), nullable=False)
    instahandle: str = Column(type_=String(length=30), nullable=True)
    image: str = Column(type_=String(length=36), nullable=True)
    auth_user_id: str = Column(type_=String(length=64), nullable=False, unique=True)

    def as_dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "name": self.name,
            "description": self.description,
            "website": self.website,
            "email": self.email,
            "instahandle": self.instahandle,
            "image": self.image,
            "auth_user_id": self.auth_user_id
        }


def brand_from_dict(brand):
    auth_user_id = ""
    if "auth_user_id" in brand:
        auth_user_id = brand["auth_user_id"]
    if 'image' in brand:
        image_id = brand['image']
    else:
        image_id = None
    return Brand(name=brand["name"],
                 description=brand["description"],
                 website=brand["website"],
                 email=brand["email"],
                 instahandle=brand["instahandle"],
                 image=image_id,
                 auth_user_id=auth_user_id)
