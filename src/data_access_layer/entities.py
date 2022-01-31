import json

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

INFLUENCER_TBL_NAME = 'influencer'
BRAND_TBL_NAME = 'brand'

Base = declarative_base()


class BaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)

    def from_dto(self, dto):
        self.id = dto.id
        self.created = dto.created


class BaseUserEntity(BaseEntity):
    first_name = Column(type_=String(length=120), nullable=False)
    last_name = Column(type_=String(length=120), nullable=False)
    email = Column(type_=String(length=120), nullable=False)
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)

    def from_dto(self, dto):
        super().from_dto(dto=dto)
        self.first_name = dto.first_name
        self.last_name = dto.last_name
        self.email = dto.email
        self.auth_user_id = dto.auth_user_id


class BrandEntity(Base, BaseUserEntity):
    __tablename__ = BRAND_TBL_NAME

    @staticmethod
    def brand_from_dto(dto=None):
        return BrandEntity().from_dto(dto)

    def from_dto(self, dto):
        super().from_dto(dto=dto)
        self.name = dto.name
        self.description = dto.description
        self.header_image = dto.header_image
        self.values = json.dumps(list(map(lambda x: x.name, dto.values)))
        self.categories = json.dumps(list(map(lambda x: x.name, dto.categories)))
        self.instahandle = dto.instahandle
        self.website = dto.website
        self.logo = dto.logo
        return self

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
