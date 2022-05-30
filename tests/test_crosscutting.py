from unittest import TestCase

from src.crosscutting import JsonSnakeToCamelSerializer


class TestJsonSnakeToCamelSerializer(TestCase):

    def setUp(self):
        self.__json_snake_to_camel_serializer = JsonSnakeToCamelSerializer()

    def test_serialize(self):
        input_data = {
            "name": "adam raymond",
            "snake_in_value": "snake_in_value",
            "value_2_to_3_values": 2
        }

        expected =\
            "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}"

        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        assert expected == actual
