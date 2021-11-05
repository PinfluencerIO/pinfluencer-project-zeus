import dataclasses
import json

import src.domain.models.base_model as base


class ModelExtensions:
    @staticmethod
    def list_to_json(models) -> str:
        """
        @type models: list[base.BaseModel]
        """
        return json.dumps(list(map(ModelExtensions.as_dict, models)), indent=4)

    @staticmethod
    def as_dict(model) -> dict:
        """
        @type model: base.BaseModel
        """
        return dataclasses.asdict(model)

    @staticmethod
    def list_to_dict(models) -> list[dict]:
        """
        @type models: list[base.BaseModel]
        """
        return list(map(ModelExtensions.as_dict, models))
