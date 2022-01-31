import json

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

INFLUENCER_TBL_NAME = 'influencer'
BRAND_TBL_NAME = 'brand'

Base = declarative_base()


class BaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)


class BaseUserEntity(BaseEntity):
    first_name = Column(type_=String(length=120), nullable=False)
    last_name = Column(type_=String(length=120), nullable=False)
    email = Column(type_=String(length=120), nullable=False)
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


class BrandEntity(Base, BaseUserEntity):
    __tablename__ = BRAND_TBL_NAME

    @staticmethod
    def from_dto(dto=None):
        brand = BrandEntity()
        brand.id = dto.id
        brand.created = dto.created
        brand.first_name = dto.first_name
        brand.last_name = dto.last_name
        brand.email = dto.email
        brand.auth_user_id = dto.auth_user_id
        brand.name = dto.name
        brand.description = dto.description
        brand.header_image = dto.header_image
        brand.values = json.dumps(list(map(lambda x: x.name, dto.values)))
        brand.categories = json.dumps(list(map(lambda x: x.name, dto.categories)))
        brand.instahandle = dto.instahandle
        brand.website = dto.website
        brand.logo = dto.logo
        return brand

    name = Column(type_=String(length=120), nullable=False)
    description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=36), nullable=True)
    values = Column(type_=String(length=120), nullable=False)
    categories = Column(type_=String(length=120), nullable=False)
    instahandle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=36), nullable=True)


class InfluencerEntity(Base, BaseUserEntity):
    __tablename__ = INFLUENCER_TBL_NAME

    instahandle = Column(type_=String(length=30), nullable=True)
    name = Column(type_=String(length=120), nullable=False)
    website = Column(type_=String(length=120), nullable=False)
    bio = Column(type_=String(length=500), nullable=False)
    image = Column(type_=String(length=36), nullable=True)
    audience_age_split = Column(type_=String(length=120), nullable=True)
    audience_gender_split = Column(type_=String(length=120), nullable=True)
    values = Column(type_=String(length=120), nullable=False)
    categories = Column(type_=String(length=120), nullable=False)
