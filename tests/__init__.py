from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import Base
from src.data.entities import BrandEntity, BaseEntity
from src.domain.models import Brand, Influencer, ValueEnum, CategoryEnum

TEST_DEFAULT_BRAND_LOGO = "default_brand_logo.png"
TEST_DEFAULT_BRAND_HEADER_IMAGE = "default_brand_header_image.png"
TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE = "default_influencer_profile_image.png"


def get_entity_dict(entity: BaseEntity) -> dict:
    dict = entity.__dict__
    dict.pop('_sa_instance_state')
    return dict


def brand_generator(dto, mapper):
    brand = mapper.map(dto, BrandEntity)
    return brand


def brand_dto_generator(num):
    if num == 1:
        values = [ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7]
    elif num == 2:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION]
    else:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE, ValueEnum.VEGAN]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION,
                      CategoryEnum.PET]
    return Brand(
        first_name=f"first_name{num}",
        last_name=f"last_name{num}",
        email=f"email{num}",
        auth_user_id=f'1234brand{num}',
        brand_name=f"name{num}",
        brand_description=f"description{num}",
        website=f"website{num}",
        insta_handle=f"instahandle{num}",
        values=values,
        categories=categories
    )


def influencer_dto_generator(num):
    if num == 1:
        values = [ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7]
    elif num == 2:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION]
    else:
        values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE, ValueEnum.VEGAN]
        categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8, CategoryEnum.FASHION,
                      CategoryEnum.PET]
    return Influencer(
        first_name=f"first_name{num}",
        last_name=f"last_name{num}",
        email=f"email{num}",
        auth_user_id=f'1234brand{num}',
        bio=f"bio{num}",
        website=f"website{num}",
        insta_handle=f"instahandle{num}",
        values=values,
        categories=categories,
        audience_age_13_to_17_split=0.14,
        audience_age_18_to_24_split=0.14,
        audience_age_25_to_34_split=0.14,
        audience_age_35_to_44_split=0.14,
        audience_age_45_to_54_split=0.14,
        audience_age_55_to_64_split=0.15,
        audience_age_65_plus_split=0.15,
        audience_male_split=0.75,
        audience_female_split=0.25
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
    for field in brand_brand_updatable_fields():
        assert brand1[field] == brand2[field]
        print(f'asserted {field} is valid')


def assert_brand_updatable_fields_are_equal_for_three(brand1, brand2, brand3):
    for field in brand_brand_updatable_fields():
        assert brand1[field] == brand2[field] == brand3[field]
        print(f'asserted {field} is valid')


def brand_brand_updatable_fields():
    return ['insta_handle', 'first_name', 'last_name', 'email', 'brand_name', 'brand_description', 'website']
