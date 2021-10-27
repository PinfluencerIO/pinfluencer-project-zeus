from abc import ABC
from datetime import datetime


class ModelBase(ABC):
    id: str
    created: datetime
    last_updated: datetime
