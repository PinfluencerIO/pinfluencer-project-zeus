import datetime
from dataclasses import dataclass

from src.domain.models import ValueEnum, CategoryEnum, CampaignStateEnum


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
    first_name: str = None
    last_name: str = None
    email: str = None


@dataclass(unsafe_hash=True)
class CampaignRequestDto:
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


@dataclass(unsafe_hash=True)
class InfluencerRequestDto:
    insta_handle: str = None
    website: str = None
    bio: str = None
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
    first_name: str = None
    last_name: str = None
    email: str = None


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
    first_name: str = None
    last_name: str = None
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


@dataclass(unsafe_hash=True)
class CampaignResponseDto(BaseResponseDto):
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
