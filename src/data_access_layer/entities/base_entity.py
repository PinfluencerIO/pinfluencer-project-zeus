import uuid
from abc import ABC
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseMeta = declarative_base()


class BaseEntity:

    __tablename__: str

    id: str = Column(type_=String(length=36), primary_key=True, default=uuid.uuid4, nullable=False)
    created: datetime = Column(DateTime, nullable=False)
