from unittest import TestCase

from src.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeCaseDeserializer

TEST_DICT_JSON = "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}"
TEST_DICT_JSON_WITH_CAPS_KEY = "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2, \"capitalLETTERSValue\": 1}"

TEST_DICT = {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2
}


TEST_DICT_WITH_CAPS_KEY = {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2,
    "capital_letters_value": 1
}


class TestJsonSnakeToCamelSerializer(TestCase):

    def setUp(self):
        self.__json_snake_to_camel_serializer = JsonSnakeToCamelSerializer()

    def test_serialize(self):

        input_data = TEST_DICT
        expected = TEST_DICT_JSON

        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        assert expected == actual


class TestJsonCamelToSnakeCaseDeserializer(TestCase):

    def setUp(self):
        self.__json_camel_to_snake_case_deserializer = JsonCamelToSnakeCaseDeserializer()

    def test_deserialize(self):

        expected = TEST_DICT_WITH_CAPS_KEY
        input_data = TEST_DICT_JSON_WITH_CAPS_KEY

        actual = self.__json_camel_to_snake_case_deserializer.deserialize(input_data)

        assert expected == actual
