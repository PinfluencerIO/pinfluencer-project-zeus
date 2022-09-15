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
