from enum import Enum
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.crosscutting import JsonSnakeToCamelSerializer
from src.data import Base
from src.data.entities import SqlAlchemyBrandEntity, SqlAlchemyBaseEntity, SqlAlchemyInfluencerEntity, \
    SqlAlchemyCampaignEntity
from src.domain.models import Brand, Influencer, ValueEnum, CategoryEnum, User, Campaign

TEST_DEFAULT_PRODUCT_IMAGE1 = "default_product_image1.png"
TEST_DEFAULT_PRODUCT_IMAGE2 = "default_product_image2.png"
TEST_DEFAULT_PRODUCT_IMAGE3 = "default_product_image3.png"
TEST_DEFAULT_BRAND_LOGO = "default_brand_logo.png"
TEST_DEFAULT_BRAND_HEADER_IMAGE = "default_brand_header_image.png"
TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE = "default_influencer_profile_image.png"


def get_entity_dict(entity: SqlAlchemyBaseEntity) -> dict:
    dict = entity.__dict__
    dict.pop('_sa_instance_state')
    return dict


def campaign_generator(dto, mapper):
    campaign = mapper.map(dto, SqlAlchemyCampaignEntity)
    return campaign


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


def brand_dto_generator(num, repo: RepoEnum = RepoEnum.NO_REPO):
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


def influencer_dto_generator(num, repo: RepoEnum = RepoEnum.NO_REPO):
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
    address = f"address{num}"
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
        address = ""
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
        audience_female_split=audience_female_split,
        address=address
    )


def campaign_dto_generator(num: int) -> Campaign:
    if num == 1:
        campaign_values = [ValueEnum.VALUE5, ValueEnum.VALUE6, ValueEnum.VALUE7]
        campaign_categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5, CategoryEnum.CATEGORY7]
    elif num == 2:
        campaign_values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE]
        campaign_categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8,
                               CategoryEnum.FASHION]
    else:
        campaign_values = [ValueEnum.VALUE5, ValueEnum.RECYCLED, ValueEnum.VALUE7, ValueEnum.SUSTAINABLE,
                           ValueEnum.VEGAN]
        campaign_categories = [CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY9, CategoryEnum.CATEGORY8,
                               CategoryEnum.FASHION,
                               CategoryEnum.PET]

    return Campaign(
        brand_id=f"brand_id{num}",
        objective=f"objective{num}",
        success_description=f"success_description{num}",
        campaign_title=f"campaign_title{num}",
        campaign_description=f"campaign_description{num}",
        campaign_categories=campaign_categories,
        campaign_values=campaign_values,
        campaign_product_link=f"campaign_product_link{num}",
        campaign_hashtag=f"campaign_hashtag{num}",
        campaign_discount_code=f"campaign_discount_code{num}",
        product_title=f"product_title{num}",
        product_description=f"product_description{num}",
        product_image1=f"product_image1{num}",
        product_image2=f"product_image2{num}",
        product_image3=f"product_image3{num}"
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


def assert_campaign_creatable_fields_are_equal_for_three(campaigns: list[dict]):
    for campaign in campaigns:
        campaign.pop("brand_id")
        campaign.pop("id")
        campaign.pop("created")
        campaign.pop("product_image1")
        campaign.pop("product_image2")
        campaign.pop("product_image3")

    assert campaigns[0] == campaigns[1] == campaigns[2]


def assert_campaign_db_fields_are_equal_for_three(campaign1: dict, campaign2: dict, campaign3: dict):
    campaign1.pop("brand_id")
    campaign2.pop("brand_id")
    campaign3.pop("brand_id")
    assert campaign1 == campaign2 == campaign3


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


def campaign_db_fields():
    return [
        "objective",
        "success_description",
        "campaign_title",
        "campaign_description",
        "campaign_categories",
        "campaign_values",
        "campaign_product_link",
        "campaign_hashtag",
        "campaign_discount_code",
        "product_title",
        "product_description",
        "campaign_state"
    ]


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
            'categories',
            'address']


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
            'insta_handle',
            'address']


def assert_brand_db_fields_are_equal(brand1: dict, brand2: dict):
    for field in brand_db_fields():
        assert brand1[field] == brand2[field]
        print(f'asserted {field} is valid')


def assert_influencer_db_fields_are_equal(influencer1: dict, influencer2: dict):
    for field in influencer_db_fields():
        assert influencer1[field] == influencer2[field]
        print(f'asserted {field} is valid')


def assert_campaign_db_fields_are_equal(campaign1: dict, campaign2: dict):
    for field in campaign_db_fields():
        assert campaign1[field] == campaign2[field]
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


def get_influencer_id_event(id):
    return {'pathParameters': {'influencer_id': id}}


def get_brand_id_event(brand_id):
    return {'pathParameters': {'brand_id': brand_id}}


def get_campaign_id_event(campaign_id):
    return {'pathParameters': {'campaign_id': campaign_id}}


def get_auth_user_event(auth_id):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"username": auth_id}}}}}


def update_brand_payload():
    return {
        "first_name": "",
        "last_name": "",
        "email": "",
        "brand_name": "name",
        "brand_description": "description",
        "website": "https://website.com",
        "insta_handle": "instahandle",
        "values": ["VALUE7", "VALUE8", "VALUE9"],
        "categories": ["CATEGORY7", "CATEGORY6", "CATEGORY5"]
    }


def update_user_dto():
    return User(first_name="first_name",
                last_name="last_name",
                email="email@gmail.com")


def create_brand_dto():
    return Brand(first_name="",
                 last_name="",
                 email="",
                 brand_name="name",
                 brand_description="description",
                 website="https://website.com",
                 insta_handle="instahandle",
                 values=[ValueEnum.VALUE7, ValueEnum.VALUE8, ValueEnum.VALUE9],
                 categories=[CategoryEnum.CATEGORY7, CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5],
                 auth_user_id="1234")


def update_image_payload():
    return {
        "image_bytes": "random_bytes"
    }


def update_brand_return_dto():
    return Brand(first_name="",
                 last_name="",
                 email="",
                 brand_name="name",
                 brand_description="description",
                 website="https://website.com",
                 insta_handle="instahandle",
                 values=[ValueEnum.VALUE7, ValueEnum.VALUE8, ValueEnum.VALUE9],
                 categories=[CategoryEnum.CATEGORY7, CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5])


def update_brand_expected_dto():
    return Brand(first_name="first_name",
                 last_name="last_name",
                 email="email@gmail.com",
                 brand_name="name",
                 brand_description="description",
                 website="https://website.com",
                 insta_handle="instahandle",
                 values=[ValueEnum.VALUE7, ValueEnum.VALUE8, ValueEnum.VALUE9],
                 categories=[CategoryEnum.CATEGORY7, CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5])


def create_for_auth_user_event(auth_id, payload):
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": auth_id}}}},
        "body": JsonSnakeToCamelSerializer().serialize(payload)
    }


def create_influencer_dto():
    return Influencer(first_name="",
                      last_name="",
                      email="",
                      bio="bio",
                      website="https://website.com",
                      insta_handle="instahandle",
                      values=[ValueEnum.VALUE7, ValueEnum.VALUE8, ValueEnum.VALUE9],
                      categories=[CategoryEnum.CATEGORY7, CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5],
                      auth_user_id="1234",
                      audience_male_split=0.5,
                      audience_female_split=0.5,
                      audience_age_13_to_17_split=0.142,
                      audience_age_18_to_24_split=0.142,
                      audience_age_25_to_34_split=0.142,
                      audience_age_35_to_44_split=0.142,
                      audience_age_45_to_54_split=0.142,
                      audience_age_55_to_64_split=0.142,
                      audience_age_65_plus_split=0.143)


def update_influencer_payload():
    return {
        "first_name": "first_name",
        "last_name": "first_name",
        "email": "email@gmail.com",
        "bio": "bio",
        "website": "https://website.com",
        "insta_handle": "instahandle",
        "values": ["VALUE7", "VALUE8", "VALUE9"],
        "categories": ["CATEGORY7", "CATEGORY6", "CATEGORY5"],
        "auth_user_id": "1234",
        "audience_male_split": 0.5,
        "audience_female_split": 0.5,
        "audience_age_13_to_17_split": 0.142,
        "audience_age_18_to_24_split": 0.142,
        "audience_age_25_to_34_split": 0.142,
        "audience_age_35_to_44_split": 0.142,
        "audience_age_45_to_54_split": 0.142,
        "audience_age_55_to_64_split": 0.142,
        "audience_age_65_plus_split": 0.143,
        "address": "69 beans road"
    }
