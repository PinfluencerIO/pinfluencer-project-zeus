import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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


@dataclass(unsafe_hash=True)
class DataModel:
    id: str = field(default_factory=uuid4_str)
    created: datetime = field(default_factory=datetime.utcnow)


@dataclass(unsafe_hash=True)
class Brand(DataModel):
    brand_name: str = None
    brand_description: str = None
    website: str = None
    logo: str = None
    header_image: str = None
    insta_handle: str = None
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    auth_user_id: str = None


@dataclass(unsafe_hash=True)
class User:
    given_name: str = None
    family_name: str = None
    email: str = None


@dataclass(unsafe_hash=True)
class Influencer(DataModel):
    insta_handle: str = None
    website: str = None
    bio: str = None
    image: str = None
    audience_age_13_to_17_split: float = None
    audience_age_18_to_24_split: float = None
    audience_age_25_to_34_split: float = None
    audience_age_35_to_44_split: float = None
    audience_age_45_to_54_split: float = None
    audience_age_55_to_64_split: float = None
    audience_age_65_plus_split: float = None
    audience_male_split: float = None
    audience_female_split: float = None
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    address: str = None
    auth_user_id: str = None


class CampaignStateEnum(Enum):
    DRAFT = "DRAFT",
    ACTIVE = "ACTIVE",
    CLOSED = "CLOSED",
    DELETED = "DELETED"


@dataclass(unsafe_hash=True)
class Campaign(DataModel):
    brand_id: str = None
    objective: str = None
    success_description: str = None
    campaign_title: str = None
    campaign_description: str = None
    campaign_categories: list[CategoryEnum] = None
    campaign_values: list[ValueEnum] = None
    campaign_state: CampaignStateEnum = None
    campaign_product_link: str = None
    campaign_hashtag: str = None
    campaign_discount_code: str = None
    product_title: str = None
    product_description: str = None
    product_image: str = None
