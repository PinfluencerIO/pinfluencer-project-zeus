import json


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))


class JsonSnakeToCamelSerializer:

    def serialize(self, data: dict) -> str:
        return json.dumps({self.__snake_case_key_to_camel_case(k): v for k, v in data.items()})

    def __snake_case_key_to_camel_case(self, key: str) -> str:
        components = key.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


class JsonCamelToSnakeCaseDeserializer:

    def deserialize(self, data: str) -> dict:
        return {}
