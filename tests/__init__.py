from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import Base
from src.data.entities import BrandEntity
from src.domain.models import Brand, Influencer, ValueEnum, CategoryEnum, AudienceAge, AudienceGender, GenderEnum

TEST_DEFAULT_BRAND_LOGO = "default_brand_logo.png"
TEST_DEFAULT_BRAND_HEADER_IMAGE = "default_brand_header_image.png"
TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE = "default_influencer_profile_image.png"


def brand_generator(dto):
    return BrandEntity.create_from_dto(dto=dto)


def brand_dto_generator(num):
    if num == 1:
        values = [ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7]
    elif num == 2:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION]
    else:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE, ValueEnum.VEGAN]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION, CategoryEnum.PET]
    return Brand(
        first_name=f"first_name{num}",
        last_name=f"last_name{num}",
        email=f"email{num}",
        auth_user_id=f'1234brand{num}',
        name=f"name{num}",
        description=f"description{num}",
        website=f"website{num}",
        logo=f'logo{num}.png',
        header_image=f'header_image{num}.png',
        instahandle=f"instahandle{num}",
        values=values,
        categories=categories
    )


def influencer_dto_generator(num):
    return Influencer(
        first_name=f"first_name{num}",
        last_name=f"last_name{num}",
        email=f"email{num}",
        auth_user_id=f'1234brand{num}',
        name=f"name{num}",
        bio=f"bio{num}",
        website=f"website{num}",
        image=f'logo{num}.png',
        instahandle=f"instahandle{num}",
        values=[ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7],
        categories=[CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7],
        audience_age_split=[AudienceAge(min=13, max=17, value=0.14),
                            AudienceAge(min=18, max=24, value=0.14),
                            AudienceAge(min=25, max=34, value=0.14),
                            AudienceAge(min=35, max=44, value=0.14),
                            AudienceAge(min=45, max=54, value=0.14),
                            AudienceAge(min=55, max=64, value=0.15),
                            AudienceAge(min=65, value=0.5)],
        audience_gender_split=[AudienceGender(gender=GenderEnum.MALE, value=0.75),
                               AudienceGender(gender=GenderEnum.FEMALE, value=0.25)]
    )


class InMemorySqliteDataManager:

    def __init__(self):
        self.__engine = create_engine('sqlite:///:memory:')
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        Base.metadata.create_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def create_fake_data(self, objects):
        self.__session.bulk_save_objects(objects=objects)


class StubDataManager:
    @property
    def engine(self):
        return Mock()

    @property
    def session(self):
        return Mock()


def assert_brand_updatable_fields_are_equal(brand1, brand2):
    assert brand1['instahandle'] == brand2['instahandle']
    assert brand1['first_name'] == brand2['first_name']
    assert brand1['last_name'] == brand2['last_name']
    assert brand1['email'] == brand2['email']
    assert brand1['name'] == brand2['name']
    assert brand1['description'] == brand2['description']
    assert brand1['website'] == brand2['website']
