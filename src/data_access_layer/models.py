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
    instahandle = ""
    name = ""
    website = ""
    bio = ""
    image = ""
    audience_age_split = []
    audience_gender_split = []
    values = []
    categories = []
