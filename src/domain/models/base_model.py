import dataclasses
import json
from abc import ABC
from dataclasses import dataclass
from datetime import datetime

import src.domain.models.model_extensions as ext


@dataclass
class BaseModel(ABC):
    id: str
    created: datetime

    def as_dict(self) -> dict:
        return ext.ModelExtensions.as_dict(self)
