from dataclasses import dataclass

from sqlalchemy import String, Column, ARRAY

from src.data_access_layer import Base, BRAND_TBL_NAME, BaseUser, ValueEnum, CategoryEnum


@dataclass
class Brand(Base, BaseUser):
    __tablename__ = BRAND_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    header_image: str = Column(type_=String(length=36), nullable=True)
    values: list[ValueEnum] = Column(type_=ARRAY(String), nullable=False)
    categories: list[CategoryEnum] = Column(type_=ARRAY(String), nullable=False)
    instahandle: str = Column(type_=String(length=30), nullable=True)
    website: str = Column(type_=String(length=120), nullable=False)
    logo: str = Column(type_=String(length=36), nullable=True)

    # TODO: implement
    def as_dict(self):
        dict = super().as_dict()
        dict.update({
            "name": self.name,
            "description": self.description,
            "header_image": self.header_image,
            "values": self.values,
            "categories": self.categories,
            "instahandle": self.instahandle,
            "website": self.website,
            "logo": self.logo
        })
        return dict


# TODO: implement
def brand_from_dict(brand):
    auth_user_id = ""
    if "auth_user_id" in brand:
        auth_user_id = brand["auth_user_id"]
    if 'image' in brand:
        image_id = brand['image']
    else:
        image_id = None
    return Brand()
