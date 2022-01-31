import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


def uuid4_str():
    return str(uuid.uuid4())


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass
class Metric:
    value: float = 0.0


@dataclass
class AudienceAge(Metric):
    min: int = 0
    max: int = 0


@dataclass
class AudienceGender(Metric):
    gender: GenderEnum = GenderEnum.MALE


class ValueEnum(Enum):
    SUSTAINABLE = "SUSTAINABLE"
    ORGANIC = "ORGANIC"
    RECYCLED = "RECYCLED"
    VEGAN = "VEGAN"
    VALUE5 = "VALUE5"
    VALUE6 = "VALUE6"
    VALUE7 = "VALUE7"
    VALUE8 = "VALUE8"
    VALUE9 = "VALUE9"
    VALUE10 = "VALUE10"


class CategoryEnum(Enum):
    FOOD = "FOOD"
    FASHION = "FASHION"
    FITNESS = "FITNESS"
    PET = "PET"
    CATEGORY5 = "CATEGORY5"
    CATEGORY6 = "CATEGORY6"
    CATEGORY7 = "CATEGORY7"
    CATEGORY8 = "CATEGORY8"
    CATEGORY9 = "CATEGORY9"
    CATEGORY10 = "CATEGORY10"


class Model:
    id = uuid4_str()
    created = datetime.utcnow()


@dataclass
class User(Model):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    auth_user_id: str = ""


@dataclass
class Brand(User):
    name: str = ""
    description: str = ""
    website: str = ""
    logo: str = ""
    header_image: str = ""
    instahandle: str = ""
    values: list[ValueEnum] = field(default_factory=list)
    categories: list[CategoryEnum] = field(default_factory=list)


@dataclass
class Influencer(User):
    instahandle: str = ""
    name: str = ""
    website: str = ""
    bio: str = ""
    image: str = ""
    audience_age_split: list[AudienceAge] = field(default_factory=list)
    audience_gender_split: list[AudienceGender] = field(default_factory=list)
    values: list[ValueEnum] = field(default_factory=list)
    categories: list[CategoryEnum] = field(default_factory=list)
