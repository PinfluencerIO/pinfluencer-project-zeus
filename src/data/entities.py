import sqlalchemy.orm
from sqlalchemy import Column, String, DateTime, Float, PickleType, Table, Integer, Boolean

from src.data import Base
from src.domain.models import Brand, Influencer, Campaign, Collaboration, Notification


class SqlAlchemyBaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)


class SqlAlchemyBaseUserEntity(SqlAlchemyBaseEntity):
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


brand_table = Table('brand', Base.metadata,
                    Column('id', String(length=36), primary_key=True),
                    Column('created', DateTime),
                    Column('auth_user_id', String(length=64)),
                    Column('brand_name', String(length=120)),
                    Column('brand_description', String(length=500)),
                    Column('header_image', String(length=360)),
                    Column('values', PickleType),
                    Column('categories', PickleType),
                    Column('insta_handle', String(length=30)),
                    Column('website', String(length=120)),
                    Column('logo', String(length=360)))

influencer_table = Table('influencer', Base.metadata,
                         Column('id', String(length=36), primary_key=True),
                         Column('created', DateTime),
                         Column('auth_user_id', String(length=64)),
                         Column('website', String(length=120)),
                         Column('bio', String(length=500)),
                         Column('image', String(length=360)),
                         Column('audience_age_13_to_17_split', Float),
                         Column('audience_age_18_to_24_split', Float),
                         Column('audience_age_25_to_34_split', Float),
                         Column('audience_age_35_to_44_split', Float),
                         Column('audience_age_45_to_54_split', Float),
                         Column('audience_age_55_to_64_split', Float),
                         Column('audience_age_65_plus_split', Float),
                         Column('audience_male_split', Float),
                         Column('audience_female_split', Float),
                         Column('insta_handle', String(length=30)),
                         Column('address', String(length=500)),
                         Column('values', PickleType),
                         Column('categories', PickleType))

campaign_table = Table('campaign', Base.metadata,
                       Column('id', String(length=36), primary_key=True),
                       Column('created', DateTime),
                       Column('brand_auth_user_id', String(length=360)),
                       Column('objective', String(length=120)),
                       Column('success_description', String(length=500)),
                       Column('campaign_title', String(length=120)),
                       Column('campaign_description', String(length=500)),
                       Column('campaign_categories', PickleType),
                       Column('campaign_values', PickleType),
                       Column('campaign_state', PickleType),
                       Column('campaign_product_link', String(length=120)),
                       Column('campaign_hashtag', String(length=120)),
                       Column('campaign_discount_code', String(length=120)),
                       Column('product_title', String(length=120)),
                       Column('product_description', String(length=500)),
                       Column('product_image', String(length=360)))

collaboration_table = Table('collaboration', Base.metadata,
                            Column('id', String(length=36), primary_key=True),
                            Column('created', DateTime),
                            Column('brand_auth_user_id', String(length=64)),
                            Column('influencer_auth_user_id', String(length=64)),
                            Column('request_details', String(length=500)),
                            Column('creative_idea', String(length=500)),
                            Column('number_of_pictures', Integer),
                            Column('number_of_videos', Integer),
                            Column('number_of_stories', Integer),
                            Column('campaign_id', PickleType),
                            Column('collaboration_state', PickleType))

notifications_table = Table('notifications', Base.metadata,
                            Column('id', String(length=36), primary_key=True),
                            Column('created', DateTime),
                            Column('sender_auth_user_id', String(length=64)),
                            Column('receiver_auth_user_id', String(length=64)),
                            Column('payload_body', String(length=500)),
                            Column('read', Boolean))


def create_mappings(logger):
    try:
        # sqlalchemy mappings
        sqlalchemy.orm.mapper(Brand, brand_table)
        sqlalchemy.orm.mapper(Influencer, influencer_table)
        sqlalchemy.orm.mapper(Campaign, campaign_table)
        sqlalchemy.orm.mapper(Collaboration, collaboration_table)
        sqlalchemy.orm.mapper(Notification, notifications_table)
    except Exception as e:
        logger.log_error(f"mappings tried to be created more than once")
        logger.log_exception(e)
