from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseModel(ABC):
    id: str
    created: datetime
