from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ModelBase(ABC):
    id: str
    created: datetime
    last_updated: datetime
