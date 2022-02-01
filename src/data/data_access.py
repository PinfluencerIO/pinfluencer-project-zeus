import json

from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

from src.domain.models import Brand, ValueEnum, CategoryEnum, AudienceAge, AudienceGender, GenderEnum, \
    Influencer

Base = declarative_base()


class BaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)

    def _from_dto(self, dto):
        self.id = dto.id
        self.created = dto.created

    def as_dto(self, dto):
        dto.id = self.id
        dto.created = self.created


class BaseUserEntity(BaseEntity):
    first_name = Column(type_=String(length=120), nullable=False)
    last_name = Column(type_=String(length=120), nullable=False)
    email = Column(type_=String(length=120), nullable=False)
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)

    def _from_dto(self, dto):
        super()._from_dto(dto=dto)
        self.first_name = dto.first_name
        self.last_name = dto.last_name
        self.email = dto.email
        self.auth_user_id = dto.auth_user_id

    def as_dto(self, dto):
        super().as_dto(dto=dto)
        dto.first_name = self.first_name
        dto.last_name = self.last_name
        dto.email = self.email
        dto.auth_user_id = self.auth_user_id


class BrandEntity(Base, BaseUserEntity):
    __tablename__ = 'brand'

    @staticmethod
    def create_from_dto(dto=None):
        return BrandEntity().from_dto(dto)

    def from_dto(self, dto):
        super()._from_dto(dto=dto)
        self.name = dto.name
        self.description = dto.description
        self.header_image = dto.header_image
        self.values = json.dumps(list(map(lambda x: x.name, dto.values)))
        self.categories = json.dumps(list(map(lambda x: x.name, dto.categories)))
        self.instahandle = dto.instahandle
        self.website = dto.website
        self.logo = dto.logo
        return self

    def as_dto(self, dto=None):
        if dto == None:
            dto = Brand()
        super().as_dto(dto=dto)
        dto.name = self.name
        dto.description = self.description
        dto.header_image = self.header_image
        dto.values = list(map(lambda x: ValueEnum[x], json.loads(self.values)))
        dto.categories = list(map(lambda x: CategoryEnum[x], json.loads(self.categories)))
        dto.instahandle = self.instahandle
        dto.website = self.website
        dto.logo = self.logo
        return dto

    name = Column(type_=String(length=120), nullable=False)
    description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=36), nullable=True)
    values = Column(type_=String(length=120), nullable=False)
    categories = Column(type_=String(length=120), nullable=False)
    instahandle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=36), nullable=True)


class InfluencerEntity(Base, BaseUserEntity):
    __tablename__ = 'influencer'

    @staticmethod
    def create_from_dto(dto=None):
        return InfluencerEntity().from_dto(dto)

    def from_dto(self, dto):
        super()._from_dto(dto=dto)
        self.name = dto.name
        self.website = dto.website
        self.bio = dto.bio
        self.image = dto.image
        self.audience_age_13_17_split = self.__get_audience_age_split_value(dto, 13, 17)
        self.audience_age_18_24_split = self.__get_audience_age_split_value(dto, 18, 24)
        self.audience_age_25_34_split = self.__get_audience_age_split_value(dto, 25, 34)
        self.audience_age_35_44_split = self.__get_audience_age_split_value(dto, 35, 44)
        self.audience_age_45_54_split = self.__get_audience_age_split_value(dto, 45, 54)
        self.audience_age_55_64_split = self.__get_audience_age_split_value(dto, 55, 64)
        self.audience_age_65_plus_split = self.__get_audience_age_split_value(dto, 65, 0)
        self.audience_male_split = self.__get_audience_gender_split_value(dto, GenderEnum.MALE)
        self.audience_female_split = self.__get_audience_gender_split_value(dto, GenderEnum.FEMALE)
        self.values = json.dumps(list(map(lambda x: x.name, dto.values)))
        self.categories = json.dumps(list(map(lambda x: x.name, dto.categories)))
        self.instahandle = dto.instahandle
        return self

    @staticmethod
    def __get_audience_age_split_value(dto, min, max):
        return [t.value for t in dto.audience_age_split if t.min == min and t.max == max][0]

    @staticmethod
    def __get_audience_gender_split_value(dto, gender):
        return [t.value for t in dto.audience_gender_split if t.gender == gender][0]

    def as_dto(self, dto=None):
        if dto == None:
            dto = Influencer()
        super().as_dto(dto=dto)
        dto.name = self.name
        dto.website = self.website
        dto.bio = self.bio
        dto.image = self.image
        dto.audience_age_split = [AudienceAge(min=13, max=17, value=self.audience_age_13_17_split),
                                  AudienceAge(min=18, max=24, value=self.audience_age_18_24_split),
                                  AudienceAge(min=25, max=34, value=self.audience_age_25_34_split),
                                  AudienceAge(min=35, max=44, value=self.audience_age_35_44_split),
                                  AudienceAge(min=45, max=54, value=self.audience_age_45_54_split),
                                  AudienceAge(min=55, max=64, value=self.audience_age_55_64_split),
                                  AudienceAge(min=65, value=self.audience_age_65_plus_split)]
        dto.audience_gender_split = [AudienceGender(gender=GenderEnum.MALE, value=self.audience_male_split),
                                     AudienceGender(gender=GenderEnum.FEMALE, value=self.audience_female_split)]
        dto.values = list(map(lambda x: ValueEnum[x], json.loads(self.values)))
        dto.categories = list(map(lambda x: CategoryEnum[x], json.loads(self.categories)))
        dto.instahandle = self.instahandle
        return self

    name = Column(type_=String(length=120), nullable=False)
    website = Column(type_=String(length=120), nullable=False)
    bio = Column(type_=String(length=500), nullable=False)
    image = Column(type_=String(length=36), nullable=True)
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
