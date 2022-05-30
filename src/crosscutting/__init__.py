def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))


class JsonSnakeToCamelSerializer:

    def serialize(self, data: dict) -> str:
        return ""


class JsonCamelToSnakeDeserializer:

    def deserialize(self, data: str) -> dict:
        return {}
