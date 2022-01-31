import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base

INFLUENCER_TBL_NAME = 'influencer'
BRAND_TBL_NAME = 'brand'

Base = declarative_base()


def uuid4_str():
    return str(uuid.uuid4())


class BaseEntity:
    def __init__(self, dto=None):
        self.id = dto.id
        self.created = dto.created

    id = Column(String(length=36), primary_key=True, default=uuid4_str, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)


class BaseUserEntity(BaseEntity):
    def __init__(self, dto=None):
        super().__init__(dto)
        self.first_name = dto.first_name
        self.last_name = dto.last_name
        self.email = dto.email
        self.auth_user_id = dto.auth_user_id

    first_name = Column(type_=String(length=120), nullable=False)
    last_name = Column(type_=String(length=120), nullable=False)
    email = Column(type_=String(length=120), nullable=False)
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


class BrandEntity(Base, BaseUser):
    __tablename__ = BRAND_TBL_NAME

    def __init__(self, dto=None):
        super().__init__(dto)
        self.name = dto.name
        self.description = dto.description
        self.header_image = dto.header_image
        self.values = list(map(lambda x: str(x), dto.values))
        self.categories = list(map(lambda x: str(x), dto.categories))
        self.instahandle = dto.instahandle
        self.website = dto.website
        self.logo = dto.logo

    name = Column(type_=String(length=120), nullable=False)
    description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=36), nullable=True)
    values = Column(type_=ARRAY(String), nullable=False)
    categories = Column(type_=ARRAY(String), nullable=False)
    instahandle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=36), nullable=True)


class InfluencerEntity(Base, BaseUser):
    __tablename__ = INFLUENCER_TBL_NAME

    name = Column(type_=String(length=120), nullable=False)
    description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=36), nullable=True)
    values = Column(type_=ARRAY(String), nullable=False)
    categories = Column(type_=ARRAY(String), nullable=False)
    instahandle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=36), nullable=True)

