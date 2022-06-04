import json
import re


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))


class JsonSnakeToCamelSerializer:

    def serialize(self, data: dict) -> str:
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

    def deserialize(self, data: str) -> dict:
        data_dict = json.loads(data)
        return {self.__camel_case_key_to_snake_case(k): v for k, v in data_dict.items()}

    @staticmethod
    def __camel_case_key_to_snake_case(key: str) -> str:
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', key)
        return '_'.join(map(str.lower, words))
