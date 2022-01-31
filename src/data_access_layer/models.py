from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class GenderEnum(Enum):
    Male = "Male"
    Female = "Female"


@dataclass
class Metric:
    Value: float


@dataclass
class AudienceAge(Metric):
    Min: int
    Max: int


@dataclass
class AudienceGender(Metric):
    Gender: GenderEnum


class ValueEnum(Enum):
    Sustainable = "Sustainable"
    Organic = "Organic"
    Recycled = "Recycled"
    Vegan = "Vegan"
    Value5 = "Value5"
    Value6 = "Value6"
    Value7 = "Value7"
    Value8 = "Value8"
    Value9 = "Value9"
    Value10 = "Value10"


class CategoryEnum(Enum):
    Food = "Food"
    Fashion = "Fashion"
    Fitness = "Fitness"
    Pet = "Pet"
    Category5 = "Category5"
    Category6 = "Category6"
    Category7 = "Category7"
    Category8 = "Category8"
    Category9 = "Category9"
    Category10 = "Category10"


@dataclass
class Model:
    id: str
    created: datetime


@dataclass
class User(Model):
    first_name: str
    last_name: str
    email: str
    auth_user_id: str


@dataclass
class Brand(User):
    name: str
    description: str
    website: str
    logo: str
    header_image: str
    instahandle: str
    values: list[ValueEnum]
    categories: list[CategoryEnum]


@dataclass
class Influencer(User):
    instahandle: str
    name: str
    website: str
    bio: str
    image: str
    audience_age_split: list[AudienceAge]
    audience_gender_split: list[AudienceGender]
    values: list[ValueEnum]
    categories: list[CategoryEnum]
