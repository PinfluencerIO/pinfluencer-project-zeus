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


class CollaborationState(Enum):
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RESUBMITTED = "RESUBMITTED"
    COMPLETE = "COMPLETE"


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
class Category(DataModel):
    category: CategoryEnum = None


@dataclass(unsafe_hash=True)
class Value(DataModel):
    value: ValueEnum = None


@dataclass(unsafe_hash=True)
class Brand(DataModel):
    brand_name: str = None
    brand_description: str = None
    website: str = None
    logo: str = None
    header_image: str = None
    insta_handle: str = None
    categories: list[Category] = field(default_factory=list[Category])
    values: list[Value] = field(default_factory=list[Value])
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
    categories: list[Category] = field(default_factory=list[Value])
    values: list[Value] = field(default_factory=list[Value])
    address: str = None
    auth_user_id: str = None


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"


@dataclass(unsafe_hash=True)
class AudienceAge(DataModel):
    split: float = None
    gender: GenderEnum = None


@dataclass(unsafe_hash=True)
class AudienceAgeSplit(DataModel):
    split: float = None
    min_age: int = None
    max_age: int = None


class CampaignStateEnum(Enum):
    DRAFT = "DRAFT",
    ACTIVE = "ACTIVE",
    CLOSED = "CLOSED",
    DELETED = "DELETED"


@dataclass(unsafe_hash=True)
class Campaign(DataModel):
    brand_auth_user_id: str = None
    objective: str = None
    success_description: str = None
    campaign_title: str = None
    campaign_description: str = None
    campaign_state: CampaignStateEnum = None
    campaign_categories: list[Category] = field(default_factory=list[Value])
    campaign_values: list[Value] = field(default_factory=list[Value])
    campaign_product_link: str = None
    campaign_hashtag: str = None
    campaign_discount_code: str = None
    product_title: str = None
    product_description: str = None
    product_image: str = None


@dataclass(unsafe_hash=True)
class Collaboration(DataModel):
    brand_auth_user_id: str = None
    influencer_auth_user_id: str = None
    request_details: str = None
    creative_idea: str = None
    number_of_pictures: int = None
    number_of_videos: int = None
    number_of_stories: int = None
    campaign_id: str = None
    collaboration_state: CollaborationState = None


@dataclass(unsafe_hash=True)
class Notification(DataModel):
    sender_auth_user_id: str = None
    receiver_auth_user_id: str = None
    payload_body: str = None
    read: bool = None
