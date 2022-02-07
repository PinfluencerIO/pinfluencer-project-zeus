import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.data import DEFAULT_BRAND_HEADER_IMAGE, DEFAULT_BRAND_LOGO, DEFAULT_INFLUENCER_PROFILE_IMAGE


def uuid4_str():
    return str(uuid.uuid4())


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


@dataclass
class Model:
    id: str = field(default_factory=uuid4_str)
    created: datetime = field(default_factory=datetime.utcnow)


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
    logo: str = DEFAULT_BRAND_LOGO
    header_image: str = DEFAULT_BRAND_HEADER_IMAGE
    instahandle: str = ""
    values: list[ValueEnum] = field(default_factory=list)
    categories: list[CategoryEnum] = field(default_factory=list)


@dataclass
class Influencer(User):
    instahandle: str = ""
    name: str = ""
    website: str = ""
    bio: str = ""
    image: str = DEFAULT_INFLUENCER_PROFILE_IMAGE
    audience_age_13_17_split: float = 0.0
    audience_age_18_24_split: float = 0.0
    audience_age_25_34_split: float = 0.0
    audience_age_35_44_split: float = 0.0
    audience_age_45_54_split: float = 0.0
    audience_age_55_64_split: float = 0.0
    audience_age_65_plus_split: float = 0.0
    audience_male_split: float = 0.0
    audience_female_split: float = 0.0
    values: list[ValueEnum] = field(default_factory=list)
    categories: list[CategoryEnum] = field(default_factory=list)
