from enum import Enum
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data import Base
from src.data.entities import SqlAlchemyBrandEntity, SqlAlchemyBaseEntity, SqlAlchemyInfluencerEntity
from src.domain.models import Brand, Influencer, ValueEnum, CategoryEnum, User

TEST_DEFAULT_BRAND_LOGO = "default_brand_logo.png"
TEST_DEFAULT_BRAND_HEADER_IMAGE = "default_brand_header_image.png"
TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE = "default_influencer_profile_image.png"


def get_entity_dict(entity: SqlAlchemyBaseEntity) -> dict:
    dict = entity.__dict__
    dict.pop('_sa_instance_state')
    return dict


def brand_generator(dto, mapper):
    brand = mapper.map(dto, SqlAlchemyBrandEntity)
    return brand


def influencer_generator(dto, mapper):
    influencer = mapper.map(dto, SqlAlchemyInfluencerEntity)
    return influencer


def get_as_json(status_code: int,
                body: str = "{}") -> dict:
    return {
        "statusCode": status_code,
        "body": body,
        "headers": {"Content-Type": "application/json",
                    'Access-Control-Allow-Origin': "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"},
    }


class RepoEnum(Enum):
    NO_REPO = 'NO_REPO',
    STD_REPO = 'STD_REPO',
    AUTH_REPO = 'AUTH_REPO'


def user_dto_generator(num: int) -> User:
    return User(first_name=f"first_name{num}",
                last_name=f"last_name{num}",
                email=f"email{num}",
                auth_user_id=f"1234{num}")

def brand_dto_generator(num, repo: RepoEnum=RepoEnum.NO_REPO):
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
    first_name = f"first_name{num}"
    last_name = f"last_name{num}"
    email = f"email{num}"
    auth_user_id = f'1234{num}'
    brand_name = f"name{num}"
    brand_description = f"description{num}"
    website = f"website{num}"
    insta_handle = f"instahandle{num}"
    if repo == RepoEnum.STD_REPO:
        first_name = ''
        last_name = ''
        email = ''
    if repo == RepoEnum.AUTH_REPO:
        auth_user_id = ''
        brand_name = ""
        brand_description = ""
        website = ""
        insta_handle = ""
        values = []
        categories = []
    return Brand(
        first_name=first_name,
        last_name=last_name,
        email=email,
        auth_user_id=auth_user_id,
        brand_name=brand_name,
        brand_description=brand_description,
        website=website,
        insta_handle=insta_handle,
        values=values,
        categories=categories
    )

def influencer_dto_generator(num, repo: RepoEnum=RepoEnum.NO_REPO):
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
    first_name = f"first_name{num}"
    last_name = f"last_name{num}"
    email = f"email{num}"
    auth_user_id = f'1234{num}'
    bio = f"bio{num}"
    website = f"website{num}"
    insta_handle = f"instahandle{num}"
    audience_age_13_to_17_split = 0.14
    audience_age_18_to_24_split = 0.14
    audience_age_25_to_34_split = 0.14
    audience_age_35_to_44_split = 0.14
    audience_age_45_to_54_split = 0.14
    audience_age_55_to_64_split = 0.15
    audience_age_65_plus_split = 0.15
    audience_male_split = 0.75
    audience_female_split = 0.25
    if repo == RepoEnum.STD_REPO:
        first_name = ''
        last_name = ''
        email = ''
    if repo == RepoEnum.AUTH_REPO:
        values = []
        categories = []
        auth_user_id = ''
        bio = ""
        website = ""
        insta_handle = ""
        audience_age_13_to_17_split = 0.0
        audience_age_18_to_24_split = 0.0
        audience_age_25_to_34_split = 0.0
        audience_age_35_to_44_split = 0.0
        audience_age_45_to_54_split = 0.0
        audience_age_55_to_64_split = 0.0
        audience_age_65_plus_split = 0.0
        audience_male_split = 0.0
        audience_female_split = 0.0
    return Influencer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        auth_user_id=auth_user_id,
        bio=bio,
        website=website,
        insta_handle=insta_handle,
        values=values,
        categories=categories,
        audience_age_13_to_17_split=audience_age_13_to_17_split,
        audience_age_18_to_24_split=audience_age_18_to_24_split,
        audience_age_25_to_34_split=audience_age_25_to_34_split,
        audience_age_35_to_44_split=audience_age_35_to_44_split,
        audience_age_45_to_54_split=audience_age_45_to_54_split,
        audience_age_55_to_64_split=audience_age_55_to_64_split,
        audience_age_65_plus_split=audience_age_65_plus_split,
        audience_male_split=audience_male_split,
        audience_female_split=audience_female_split
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


def assert_brand_user_generated_fields_are_equal(brand1, brand2):
    brand1.pop("id")
    brand2.pop("id")
    brand1.pop("created")
    brand2.pop("created")
    assert brand1 == brand2


def assert_influencer_creatable_generated_fields_are_equal(influencer1, influencer2):
    influencer2.pop("id")
    influencer2.pop("created")
    influencer2.pop("image")
    influencer2["categories"] = list(map(lambda x: x.name, influencer2["categories"]))
    influencer2["values"] = list(map(lambda x: x.name, influencer2["values"]))
    print("")
    print(influencer1)
    print(influencer2)
    assert influencer1 == influencer2


def assert_brand_creatable_generated_fields_are_equal(brand1, brand2):
    brand2.pop("id")
    brand2.pop("created")
    brand2.pop("auth_user_id")
    brand2.pop("logo")
    brand2.pop("header_image")
    brand2["categories"] = list(map(lambda x: x.name, brand2["categories"]))
    brand2["values"] = list(map(lambda x: x.name, brand2["values"]))
    print("")
    print(brand1)
    print(brand2)
    assert brand1 == brand2


def assert_brand_updatable_fields_are_equal(brand1, brand2):
    for field in brand_brand_updatable_fields():
        assert brand1[field] == brand2[field]
        print(f'asserted {field} is valid')


def assert_brand_updatable_fields_are_equal_for_three(brand1, brand2, brand3):
    for field in brand_brand_updatable_fields():
        assert brand1[field] == brand2[field] == brand3[field]
        print(f'asserted {field} is valid')


def brand_db_fields():
    return ['insta_handle',
            'brand_name',
            'brand_description',
            'website',
            'logo',
            'header_image',
            'values',
            'categories',
            'auth_user_id']


def influencer_db_fields():
    return ['website',
            'bio',
            'image',
            'audience_age_13_to_17_split',
            'audience_age_18_to_24_split',
            'audience_age_25_to_34_split',
            'audience_age_35_to_44_split',
            'audience_age_45_to_54_split',
            'audience_age_55_to_64_split',
            'audience_age_65_plus_split',
            'audience_male_split',
            'audience_female_split',
            'insta_handle',
            'values',
            'categories']


def influencer_update_db_fields():
    return ['website',
            'bio',
            'audience_age_13_to_17_split',
            'audience_age_18_to_24_split',
            'audience_age_25_to_34_split',
            'audience_age_35_to_44_split',
            'audience_age_45_to_54_split',
            'audience_age_55_to_64_split',
            'audience_age_65_plus_split',
            'audience_male_split',
            'audience_female_split',
            'insta_handle']


def assert_brand_db_fields_are_equal(brand1: dict, brand2: dict):
    for field in brand_db_fields():
        assert brand1[field] == brand2[field]
        print(f'asserted {field} is valid')


def assert_influencer_db_fields_are_equal(influencer1: dict, influencer2: dict):
    for field in influencer_db_fields():
        assert influencer1[field] == influencer2[field]
        print(f'asserted {field} is valid')


def assert_influencer_update_fields_are_equal(influencer1: dict, influencer2: dict):
    for field in influencer_update_db_fields():
        assert influencer1[field] == influencer2[field]
        print(f'asserted {field} is valid')


def assert_influencer_db_fields_are_equal_for_three(influencer1: dict, influencer2: dict, influencer3: dict):
    for field in influencer_db_fields():
        assert influencer1[field] == influencer2[field] == influencer3[field]
        print(f'asserted {field} is valid')


def assert_brand_db_fields_are_equal_for_three(brand1: dict, brand2: dict, brand3: dict):
    for field in brand_db_fields():
        assert brand1[field] == brand2[field] == brand3[field]
        print(f'asserted {field} is valid')


def assert_collection_brand_db_fields_are_equal(brand1: list, brand2: list):
    brand_list1 = list(map(get_db_brand, brand1))
    brand_list2 = list(map(get_db_brand, brand2))
    assert brand_list1 == brand_list2


def get_db_brand(brand: dict) -> dict:
    new_brand = {}
    for field in brand_db_fields():
        new_brand[field] = brand[field]
    return new_brand


def brand_brand_updatable_fields():
    return ['insta_handle', 'brand_name', 'brand_description', 'website']
