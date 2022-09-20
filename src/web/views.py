import datetime
from dataclasses import dataclass

from src.domain.models import ValueEnum, CategoryEnum


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

