import json
from typing import Union

from sqlalchemy import Column, String, DateTime, Float

from src.data import Base, DEFAULT_BRAND_LOGO, DEFAULT_BRAND_HEADER_IMAGE, DEFAULT_INFLUENCER_PROFILE_IMAGE
from src.domain.models import Brand, ValueEnum, CategoryEnum, AudienceAge, AudienceGender, GenderEnum, \
    Influencer
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

    name = Column(type_=String(length=120), nullable=False)
    description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=360), nullable=True)
    values = Column(type_=String(length=360), nullable=False)
    categories = Column(type_=String(length=360), nullable=False)
    instahandle = Column(type_=String(length=30), nullable=True)
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
    values = Column(type_=String(length=120), nullable=False)
    categories = Column(type_=String(length=120), nullable=False)


def get_audience_age_split_value(influencer, _min, _max):
    return [t.value for t in influencer.audience_age_split if t.min == _min and t.max == _max][0]


def get_audience_gender_split_value(influencer, gender):
    return [t.value for t in influencer.audience_gender_split if t.gender == gender][0]


def get_values(user):
    return json.dumps(list(map(lambda x: x.value, user.values)))


def get_categories(user):
    return json.dumps(list(map(lambda x: x.value, user.categories)))


def create_mappings(mapper: Union[ObjectMapperAdapter, object]):
    mapper.create_map(Brand, BrandEntity, {
        'values': get_values,
        'categories': get_categories,
        'header_image': lambda brand: DEFAULT_BRAND_HEADER_IMAGE if brand.header_image is "" else brand.header_image,
        'logo': lambda brand: DEFAULT_BRAND_LOGO if brand.logo is "" else brand.logo
    })
    mapper.create_map(BrandEntity, Brand, {
        'values': lambda brand: list(map(lambda x: ValueEnum[x], json.loads(brand.values))),
        'categories': lambda brand: list(map(lambda x: CategoryEnum[x], json.loads(brand.categories))),
        'header_image': lambda brand: DEFAULT_BRAND_HEADER_IMAGE if brand.header_image is "" else brand.header_image,
        'logo': lambda brand: DEFAULT_BRAND_LOGO if brand.logo is "" else brand.logo
    })
    mapper.create_map(Influencer, InfluencerEntity, {
        'values': get_values,
        'categories': get_categories,
        'audience_age_13_17_split': lambda influencer: get_audience_age_split_value(influencer, 13, 17),
        'audience_age_18_24_split': lambda influencer: get_audience_age_split_value(influencer, 18, 24),
        'audience_age_25_34_split': lambda influencer: get_audience_age_split_value(influencer, 25, 34),
        'audience_age_35_44_split': lambda influencer: get_audience_age_split_value(influencer, 35, 44),
        'audience_age_45_54_split': lambda influencer: get_audience_age_split_value(influencer, 45, 54),
        'audience_age_55_64_split': lambda influencer: get_audience_age_split_value(influencer, 55, 64),
        'audience_age_65_plus_split': lambda influencer: get_audience_age_split_value(influencer, 65, 0),
        'audience_male_split': lambda influencer: get_audience_gender_split_value(influencer, GenderEnum.MALE),
        'audience_female_split': lambda influencer: get_audience_gender_split_value(influencer, GenderEnum.FEMALE),
        'image': lambda influencer: DEFAULT_INFLUENCER_PROFILE_IMAGE if influencer.image is "" else influencer.image
    })
    mapper.create_map(InfluencerEntity, Influencer, {
        'values': lambda influencer: list(map(lambda x: ValueEnum[x], json.loads(influencer.values))),
        'categories': lambda influencer: list(map(lambda x: CategoryEnum[x], json.loads(influencer.categories))),
        'audience_age_split': lambda influencer: [
            AudienceAge(min=13, max=17, value=influencer.audience_age_13_17_split),
            AudienceAge(min=18, max=24, value=influencer.audience_age_18_24_split),
            AudienceAge(min=25, max=34, value=influencer.audience_age_25_34_split),
            AudienceAge(min=35, max=44, value=influencer.audience_age_35_44_split),
            AudienceAge(min=45, max=54, value=influencer.audience_age_45_54_split),
            AudienceAge(min=55, max=64, value=influencer.audience_age_55_64_split),
            AudienceAge(min=65, value=influencer.audience_age_65_plus_split)
        ],
        'audience_gender_split': lambda influencer: [
            AudienceGender(gender=GenderEnum.MALE, value=influencer.audience_male_split),
            AudienceGender(gender=GenderEnum.FEMALE, value=influencer.audience_female_split)
        ],
        'image': lambda influencer: DEFAULT_INFLUENCER_PROFILE_IMAGE if influencer.image is "" else influencer.image
    })
