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


class CollaborationStateEnum(Enum):
    APPLIED = "APPLIED"
    APPROVED = "APPROVED"
    DELIVERED = "DELIVERED"


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
class Resource:
    id: str = field(default_factory=uuid4_str)


@dataclass(unsafe_hash=True)
class DataModel(Resource):
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
    categories: list[Category] = field(default_factory=list)
    values: list[Value] = field(default_factory=list)
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
    categories: list[Category] = field(default_factory=list)
    values: list[Value] = field(default_factory=list)
    address: str = None
    auth_user_id: str = None


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"


@dataclass(unsafe_hash=True)
class AudienceGender(DataModel):
    split: float = None
    gender: GenderEnum = None
    influencer_auth_user_id: str = None


@dataclass(unsafe_hash=True)
class AudienceAge(DataModel):
    split: float = None
    min_age: int = None
    max_age: int = None
    influencer_auth_user_id: str = None


@dataclass(unsafe_hash=True)
class AudienceAgeSplit:
    audience_ages: list[AudienceAge] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class AudienceGenderSplit:
    audience_genders: list[AudienceGender] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class Listing(DataModel):
    brand_auth_user_id: str = None
    creative_guidance: str = None
    title: str = None
    categories: list[Category] = field(default_factory=list)
    values: list[Value] = field(default_factory=list)
    product_name: str = None
    product_description: str = None
    product_image: str = None


@dataclass(unsafe_hash=True)
class Collaboration(DataModel):
    brand_auth_user_id: str = None
    influencer_auth_user_id: str = None
    content_proposal: str = None
    number_of_pictures: int = None
    number_of_videos: int = None
    number_of_stories: int = None
    listing_id: str = None
    collaboration_state: CollaborationStateEnum = None


@dataclass(unsafe_hash=True)
class InfluencerCollaboration(Collaboration):
    brand: Brand = None
    listing: Listing = None


@dataclass(unsafe_hash=True)
class BrandCollaboration(Collaboration):
    influencer: Influencer = None
    listing: Listing = None


@dataclass(unsafe_hash=True)
class InfluencerListing(Listing):
    brand: Brand = None


@dataclass(unsafe_hash=True)
class BrandListing(Listing):
    approved_collaborations: list[Collaboration] = field(default_factory=list)
    delivered_collaborations: list[Collaboration] = field(default_factory=list)
    applied_collaborations: list[Collaboration] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class Notification(DataModel):
    sender_auth_user_id: str = None
    receiver_auth_user_id: str = None
    payload_body: str = None
    read: bool = None
