from typing import Union

from sqlalchemy import Column, String, DateTime, Float, PickleType

from src.data import Base
from src.domain.models import Brand, Influencer
from src.types import ObjectMapperAdapter


class BaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)


class BaseUserEntity(BaseEntity):
    first_name = Column(type_=String(length=120), nullable=False)
    last_name = Column(type_=String(length=120), nullable=False)
    email = Column(type_=String(length=120), nullable=False)
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


class BrandEntity(Base, BaseUserEntity):
    __tablename__ = 'brand'

    brand_name = Column(type_=String(length=120), nullable=False)
    brand_description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=360), nullable=True)
    values = Column(type_=PickleType, nullable=False)
    categories = Column(type_=PickleType, nullable=False)
    insta_handle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=360), nullable=True)


class InfluencerEntity(Base, BaseUserEntity):
    __tablename__ = 'influencer'

    name = Column(type_=String(length=120), nullable=False)
    website = Column(type_=String(length=120), nullable=False)
    bio = Column(type_=String(length=500), nullable=False)
    image = Column(type_=String(length=360), nullable=True)
    audience_age_13_17_split = Column(type_=Float, nullable=True)
    audience_age_18_24_split = Column(type_=Float, nullable=True)
    audience_age_25_34_split = Column(type_=Float, nullable=True)
    audience_age_35_44_split = Column(type_=Float, nullable=True)
    audience_age_45_54_split = Column(type_=Float, nullable=True)
    audience_age_55_64_split = Column(type_=Float, nullable=True)
    audience_age_65_plus_split = Column(type_=Float, nullable=True)
    audience_male_split = Column(type_=Float, nullable=True)
    audience_female_split = Column(type_=Float, nullable=True)
    instahandle = Column(type_=String(length=30), nullable=True)
    values = Column(type_=PickleType, nullable=False)
    categories = Column(type_=PickleType, nullable=False)


def create_mappings(mapper: Union[ObjectMapperAdapter, object]):
    mapper.create_map(Brand, BrandEntity)
    mapper.create_map(BrandEntity, Brand)
    mapper.create_map(Influencer, InfluencerEntity)
    mapper.create_map(InfluencerEntity, Influencer)
