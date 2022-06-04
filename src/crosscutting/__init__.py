import json
import re
from typing import Union


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))


class JsonSnakeToCamelSerializer:

    def serialize(self, data: Union[dict, list]) -> str:
        return json.dumps(self.__snake_case_to_camel_case_dict(d=data))

    def __snake_case_to_camel_case_dict(self, d):
        if isinstance(d, list):
            return [self.__snake_case_to_camel_case_dict(i) if isinstance(i, (dict, list)) else i for i in d]
        return {self.__snake_case_key_to_camel_case(a): self.__snake_case_to_camel_case_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}

    @staticmethod
    def __snake_case_key_to_camel_case(key: str) -> str:
        components = key.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


class JsonCamelToSnakeCaseDeserializer:

    def deserialize(self, data: str) -> Union[dict, list]:
        data_dict = json.loads(data)
        return self.__camel_case_to_snake_case_dict(d=data_dict)

    def __camel_case_to_snake_case_dict(self, d):
        if isinstance(d, list):
            return [self.__camel_case_to_snake_case_dict(i) if isinstance(i, (dict, list)) else i for i in d]
        return {self.__camel_case_key_to_snake_case(a): self.__camel_case_to_snake_case_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}

    @staticmethod
    def __camel_case_key_to_snake_case(key: str) -> str:
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', key)
        return '_'.join(map(str.lower, words))
