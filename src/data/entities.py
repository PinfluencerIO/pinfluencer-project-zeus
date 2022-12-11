from typing import Type

import sqlalchemy.orm
from sqlalchemy import Column, String, DateTime, Float, Table, Integer, Boolean, Enum, orm, and_
from sqlalchemy.orm import foreign

from src import T
from src.data import Base
from src.domain.models import Brand, Influencer, Listing, Collaboration, Notification, ValueEnum, Value, CategoryEnum, \
    Category, GenderEnum, AudienceAge, AudienceGender, CollaborationStateEnum, BrandListing, InfluencerListing, \
    BrandCollaboration, InfluencerCollaboration


class SqlAlchemyBaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)


class SqlAlchemyBaseUserEntity(SqlAlchemyBaseEntity):
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


value_table = Table('value', Base.metadata,
                    Column('id', String(length=36), primary_key=True),
                    Column('created', DateTime),
                    Column('value', Enum(ValueEnum)),
                    Column('brand_id', String(length=64)),
                    Column('influencer_id', String(length=64)),
                    Column('listing_id', String(length=64)))

audience_age_table = Table('audience_age', Base.metadata,
                           Column('id', String(length=36), primary_key=True),
                           Column('created', DateTime),
                           Column('min_age', Integer),
                           Column('max_age', Integer),
                           Column('split', Float),
                           Column('influencer_auth_user_id', String(length=64)))

audience_gender_table = Table('audience_gender', Base.metadata,
                              Column('id', String(length=36), primary_key=True),
                              Column('created', DateTime),
                              Column('gender', Enum(GenderEnum)),
                              Column('split', Float),
                              Column('influencer_auth_user_id', String(length=64)))

category_table = Table('category', Base.metadata,
                       Column('id', String(length=36), primary_key=True),
                       Column('created', DateTime),
                       Column('category', Enum(CategoryEnum)),
                       Column('brand_id', String(length=64)),
                       Column('influencer_id', String(length=64)),
                       Column('listing_id', String(length=64)))

brand_table = Table('brand', Base.metadata,
                    Column('id', String(length=36), primary_key=True),
                    Column('created', DateTime),
                    Column('auth_user_id', String(length=64)),
                    Column('brand_name', String(length=120)),
                    Column('brand_description', String(length=500)),
                    Column('header_image', String(length=360)),
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
                         Column('insta_handle', String(length=30)),
                         Column('address', String(length=500)))

listing_table = Table('listing', Base.metadata,
                      Column('id', String(length=36), primary_key=True),
                      Column('created', DateTime),
                      Column('brand_auth_user_id', String(length=360)),
                      Column('creative_guidance', String(length=120)),
                      Column('title', String(length=120)),
                      Column('product_name', String(length=120)),
                      Column('product_description', String(length=500)),
                      Column('product_image', String(length=360)))

collaboration_table = Table('collaboration', Base.metadata,
                            Column('id', String(length=36), primary_key=True),
                            Column('created', DateTime),
                            Column('brand_auth_user_id', String(length=64)),
                            Column('influencer_auth_user_id', String(length=64)),
                            Column('content_proposal', String(length=500)),
                            Column('number_of_pictures', Integer),
                            Column('number_of_videos', Integer),
                            Column('number_of_stories', Integer),
                            Column('listing_id', String(length=64)),
                            Column('collaboration_state', Enum(CollaborationStateEnum)))

notifications_table = Table('notification', Base.metadata,
                            Column('id', String(length=36), primary_key=True),
                            Column('created', DateTime),
                            Column('sender_auth_user_id', String(length=64)),
                            Column('receiver_auth_user_id', String(length=64)),
                            Column('payload_body', String(length=500)),
                            Column('read', Boolean))


def create_single_mappings():
    sqlalchemy.orm.mapper(AudienceGender, audience_gender_table)
    sqlalchemy.orm.mapper(AudienceAge, audience_age_table)
    sqlalchemy.orm.mapper(Value, value_table)
    sqlalchemy.orm.mapper(Category, category_table)
    sqlalchemy.orm.mapper(Brand, brand_table, properties={
        'values': create_joined_relationship(key_from=brand_table.c.auth_user_id,
                                             key_to=value_table.c.brand_id,
                                             _type=Value),
        'categories': create_joined_relationship(key_from=brand_table.c.auth_user_id,
                                                 key_to=category_table.c.brand_id,
                                                 _type=Category)
    })
    sqlalchemy.orm.mapper(Influencer, influencer_table, properties={
        'values': create_joined_relationship(key_from=influencer_table.c.auth_user_id,
                                             key_to=value_table.c.influencer_id,
                                             _type=Value),
        'categories': create_joined_relationship(key_from=influencer_table.c.auth_user_id,
                                                 key_to=category_table.c.influencer_id,
                                                 _type=Category)
    })
    sqlalchemy.orm.mapper(Listing, listing_table, properties={
        'values': create_joined_relationship(key_from=listing_table.c.id,
                                             key_to=value_table.c.listing_id,
                                             _type=Value),
        'categories': create_joined_relationship(key_from=listing_table.c.id,
                                                 key_to=category_table.c.listing_id,
                                                 _type=Category)
    })
    sqlalchemy.orm.mapper(Collaboration, collaboration_table)
    sqlalchemy.orm.mapper(Notification, notifications_table)


def create_aggregate_mappings():
    sqlalchemy.orm.mapper(InfluencerListing, listing_table, properties={
        'values': create_joined_relationship(key_from=listing_table.c.id,
                                             key_to=value_table.c.listing_id,
                                             _type=Value),
        'categories': create_joined_relationship(key_from=listing_table.c.id,
                                                 key_to=category_table.c.listing_id,
                                                 _type=Category),
        'brand': create_joined_relationship_wo_delete(key_from=brand_table.c.auth_user_id,
                                                      key_to=listing_table.c.brand_auth_user_id,
                                                      _type=Brand),
    })
    sqlalchemy.orm.mapper(BrandListing, listing_table, properties={
        'values': create_joined_relationship(key_from=listing_table.c.id,
                                             key_to=value_table.c.listing_id,
                                             _type=Value),
        'categories': create_joined_relationship(key_from=listing_table.c.id,
                                                 key_to=category_table.c.listing_id,
                                                 _type=Category),
        'delivered_collaborations': create_collab_filtered_joined_relationship(CollaborationStateEnum.DELIVERED),
        'applied_collaborations': create_collab_filtered_joined_relationship(CollaborationStateEnum.APPLIED),
        'approved_collaborations': create_collab_filtered_joined_relationship(CollaborationStateEnum.APPROVED)
    })
    sqlalchemy.orm.mapper(BrandCollaboration, collaboration_table, properties={
        'listing': create_joined_relationship_wo_delete(key_from=listing_table.c.id,
                                                        key_to=collaboration_table.c.listing_id,
                                                        _type=Listing),
        'influencer': create_joined_relationship_wo_delete(key_from=influencer_table.c.auth_user_id,
                                                           key_to=collaboration_table.c.influencer_auth_user_id,
                                                           _type=Influencer)
    })
    sqlalchemy.orm.mapper(InfluencerCollaboration, collaboration_table, properties={
        'listing': create_joined_relationship_wo_delete(key_from=listing_table.c.id,
                                                        key_to=collaboration_table.c.listing_id,
                                                        _type=Listing),
        'brand': create_joined_relationship_wo_delete(key_from=brand_table.c.auth_user_id,
                                                      key_to=collaboration_table.c.brand_auth_user_id,
                                                      _type=Brand)
    })


def create_mappings(logger):
    try:
        create_single_mappings()
        create_aggregate_mappings()
    except Exception as e:
        logger.log_error(f"mappings tried to be created more than once")
        logger.log_exception(e)


def create_joined_relationship(key_from, key_to, _type: Type[T]):
    return orm.relationship(_type,
                            foreign_keys=key_to,
                            primaryjoin=key_from == key_to,
                            lazy='joined',
                            cascade="all, delete-orphan")


def create_joined_relationship_wo_delete(key_from, key_to, _type: Type[T]):
    return orm.relationship(_type,
                            foreign_keys=key_to,
                            primaryjoin=key_from == key_to,
                            lazy='joined')


def create_collab_filtered_joined_relationship(state: CollaborationStateEnum):
    return orm.relationship(Collaboration,
                            foreign_keys=collaboration_table.c.listing_id,
                            primaryjoin=and_(listing_table.c.id == collaboration_table.c.listing_id,
                                             collaboration_table.c.collaboration_state == state),
                            lazy='joined')
