import datetime

from attr import dataclass


@dataclass()
class Brand:
    id_: str
    name: str
    description: str
    image: str
    website: str
    email: str
    auth_user_id: str
    created: datetime


@dataclass()
class Product:
    id_: str
    name: str
    description: str
    image: str
    requirements: str
    brand_id: str
    brand_name: str
    created: datetime
