from dataclasses import dataclass

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.data_access_layer import Base, PRODUCT_TBL_NAME, BRAND_TBL_NAME, BaseEntity
from src.data_access_layer.brand import Brand


@dataclass
class Product(Base, BaseEntity):
    __tablename__ = PRODUCT_TBL_NAME

    name: str = Column(type_=String(length=120), nullable=False)
    description: str = Column(type_=String(length=500), nullable=False)
    requirements: str = Column(type_=String(length=500), nullable=False)
    brand_id: str = Column(String(length=36), ForeignKey(f"{BRAND_TBL_NAME}.id"))
    brand = relationship('Brand')

    @property
    def owner(self):
        """
        @rtype: Brand
        """
        return self.brand

    def as_dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "name": self.name,
            "description": self.description,
            "requirements": self.requirements,
            "brand": {
                "id": self.owner.id,
                "name": self.owner.name
            }
        }


def product_from_dict(product: dict, nested_brand: bool, id: bool) -> Product:
    prod = Product(name=product["name"],
                   description=product["description"],
                   requirements=product["requirements"])
    if nested_brand:
        prod.brand_id = product['brand']['id']
    else:
        prod.brand_id = product['brand_id']
    if id:
        prod.id = product['id']
    return prod
