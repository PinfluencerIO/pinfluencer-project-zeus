import datetime
from dataclasses import dataclass

from src.domain.models import ValueEnum, CategoryEnum, CollaborationStateEnum


@dataclass(unsafe_hash=True)
class ImageRequestDto:
    image_path: str = None
    image_field: str = None


@dataclass(unsafe_hash=True)
class RawImageRequestDto:
    image_bytes: str = None


@dataclass(unsafe_hash=True)
class BrandRequestDto:
    brand_name: str = None
    brand_description: str = None
    website: str = None
    insta_handle: str = None
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    given_name: str = None
    family_name: str = None
    email: str = None


@dataclass(unsafe_hash=True)
class ListingRequestDto:
    creative_guidance: str = None
    title: str = None
    categories: list[CategoryEnum] = None
    values: list[ValueEnum] = None
    product_name: str = None
    product_description: str = None


@dataclass(unsafe_hash=True)
class InfluencerRequestDto:
    insta_handle: str = None
    website: str = None
    bio: str = None
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    address: str = None
    given_name: str = None
    family_name: str = None
    email: str = None


@dataclass(unsafe_hash=True)
class AudienceAgeViewDto:
    audience_age_13_to_17_split: float = None
    audience_age_18_to_24_split: float = None
    audience_age_25_to_34_split: float = None
    audience_age_35_to_44_split: float = None
    audience_age_45_to_54_split: float = None
    audience_age_55_to_64_split: float = None
    audience_age_65_plus_split: float = None


@dataclass(unsafe_hash=True)
class AudienceGenderViewDto:
    audience_male_split: float = None
    audience_female_split: float = None


@dataclass(unsafe_hash=True)
class CollaborationCreateRequestDto:
    request_details: str = None
    creative_idea: str = None
    number_of_pictures: int = None
    number_of_videos: int = None
    number_of_stories: int = None
    listing_id: str = None


@dataclass(unsafe_hash=True)
class CollaborationUpdateRequestDto:
    request_details: str = None
    creative_idea: str = None
    number_of_pictures: int = None
    number_of_videos: int = None
    number_of_stories: int = None
    collaboration_state: CollaborationStateEnum = None


@dataclass(unsafe_hash=True)
class NotificationCreateRequestDto:
    sender_auth_user_id: str = None
    receiver_auth_user_id: str = None
    payload_body: str = None
    read: bool = None


@dataclass(unsafe_hash=True)
class NotificationUpdateRequestDto:
    payload_body: str = None
    read: bool = None


@dataclass(unsafe_hash=True)
class BaseResponseDto:
    id: str = None
    created: datetime.datetime = None


@dataclass(unsafe_hash=True)
class BrandResponseDto(BaseResponseDto):
    brand_name: str = None
    brand_description: str = None
    website: str = None
    insta_handle: str = None
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    given_name: str = None
    family_name: str = None
    email: str = None
    logo: str = None
    header_image: str = None
    auth_user_id: str = None


@dataclass(unsafe_hash=True)
class InfluencerResponseDto(BaseResponseDto):
    insta_handle: str = None
    website: str = None
    bio: str = None
    image: str = None
    audience_age_13_to_17_split: float = 0.0
    audience_age_18_to_24_split: float = 0.0
    audience_age_25_to_34_split: float = 0.0
    audience_age_35_to_44_split: float = 0.0
    audience_age_45_to_54_split: float = 0.0
    audience_age_55_to_64_split: float = 0.0
    audience_age_65_plus_split: float = 0.0
    audience_male_split: float = 0.0
    audience_female_split: float = 0.0
    values: list[ValueEnum] = None
    categories: list[CategoryEnum] = None
    address: str = None
    auth_user_id: str = None


@dataclass(unsafe_hash=True)
class ListingResponseDto(BaseResponseDto):
    brand_auth_user_id: str = None
    creative_guidance: str = None
    title: str = None
    categories: list[CategoryEnum] = None
    values: list[ValueEnum] = None
    product_name: str = None
    product_description: str = None
    product_image: str = None


@dataclass(unsafe_hash=True)
class CollaborationResponseDto(BaseResponseDto):
    brand_auth_user_id: str = None
    influencer_auth_user_id: str = None
    request_details: str = None
    creative_idea: str = None
    number_of_pictures: int = None
    number_of_videos: int = None
    number_of_stories: int = None
    listing_id: str = None
    collaboration_state: CollaborationStateEnum = None


@dataclass(unsafe_hash=True)
class NotificationResponseDto(BaseResponseDto):
    receiver_auth_user_id: str = None
    sender_auth_user_id: str = None
    payload_body: str = None
    read: bool = None


