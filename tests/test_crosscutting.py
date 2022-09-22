import datetime
from dataclasses import dataclass, field
from unittest import TestCase

from src.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeCaseDeserializer, AutoFixture, \
    PinfluencerObjectMapper
from src.domain.models import ValueEnum, CategoryEnum

TEST_DICT_JSON = "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}"
TEST_LIST_SERIALIZATION_JSON = "[{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}, {\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}, {\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2}]"
TEST_LIST_SERIALIZATION_EMPTY_JSON = "[]"
TEST_DICT_NESTED_JSON = "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2, \"nestedObject\": {\"name\": \"dennis reynolds\", \"snakeValue\": 3}, \"arrayValue\": [\"apples\", \"pears\", \"oranges\"]}"
TEST_DICT_JSON_WITH_CAPS_KEY = "{\"name\": \"adam raymond\", \"snakeInValue\": \"snake_in_value\", \"value2To3Values\": 2, \"capitalLETTERSValue\": 1}"

TEST_DICT = {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2
}

TEST_LIST_SERIALIZATION_EMPTY = []

TEST_LIST_SERIALIZATION = [{
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2
}, {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2
}, {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2
}]

TEST_NESTED_DICT = {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2,
    "nested_object": {
        "name": "dennis reynolds",
        "snake_value": 3
    },
    "array_value": ["apples", "pears", "oranges"]
}

TEST_DICT_WITH_CAPS_KEY = {
    "name": "adam raymond",
    "snake_in_value": "snake_in_value",
    "value_2_to_3_values": 2,
    "capital_letters_value": 1
}


@dataclass(unsafe_hash=True)
class InheritedDto:
    id: str = field(default_factory=lambda: "default_id")
    name: str = None


@dataclass(unsafe_hash=True)
class NestedTestOtherDto:
    id: str = None
    name: str = None


@dataclass(unsafe_hash=True)
class TestOtherDto:
    id: str = None
    name: str = None
    bool_: bool = None
    enum: ValueEnum = None
    list_of_enums: list[CategoryEnum] = None
    list_of_strings: list[str] = None
    list_of_ints: list[int] = None
    list_of_floats: list[float] = None
    list_of_bools: list[bool] = None
    date: datetime.datetime = None
    list_of_dates: list[datetime.datetime] = None
    decimal_num: float = None
    nested: NestedTestOtherDto = None
    nested_list: list[NestedTestOtherDto] = None


@dataclass(unsafe_hash=True)
class NestedTestDto:
    id: str = None
    name: str = None


@dataclass(unsafe_hash=True)
class TestDto(InheritedDto):
    bool_: bool = None
    enum: ValueEnum = None
    list_of_enums: list[CategoryEnum] = None
    list_of_strings: list[str] = None
    list_of_ints: list[int] = None
    list_of_floats: list[float] = None
    list_of_bools: list[bool] = None
    date: datetime.datetime = None
    list_of_dates: list[datetime.datetime] = None
    decimal_num: float = None
    nested: NestedTestDto = None
    nested_list: list[NestedTestDto] = None


class TestPinfluencerMapper:

    def test_map(self):
        # arrange
        test_dto = AutoFixture().create(dto=TestDto,
                                        list_limit=5)

        # act
        test_other_dto: TestOtherDto = PinfluencerObjectMapper().map(_from=test_dto, to=TestOtherDto)

        # assert
        assert test_other_dto.id == "default_id"
        assert test_other_dto.date == test_dto.date
        assert test_other_dto.list_of_dates == test_dto.list_of_dates
        assert test_other_dto.name == test_dto.name
        assert test_other_dto.nested_list == test_dto.nested_list
        assert test_other_dto.nested.id == test_dto.nested.id
        assert test_other_dto.nested.name == test_dto.nested.name
        assert test_other_dto.list_of_dates == test_dto.list_of_dates
        assert test_other_dto.list_of_bools == test_dto.list_of_bools
        assert test_other_dto.list_of_ints == test_dto.list_of_ints
        assert test_other_dto.bool_ == test_dto.bool_
        assert test_other_dto.list_of_strings == test_dto.list_of_strings
        assert test_other_dto.list_of_enums == test_dto.list_of_enums
        assert test_other_dto.enum == test_dto.enum
        assert test_other_dto.decimal_num == test_dto.decimal_num
        assert test_other_dto.list_of_floats == test_dto.list_of_floats


class TestAutoFixture:

    def test_create(self):
        # arrange
        autofixture = AutoFixture()

        # act
        dto: TestDto = autofixture.create(dto=TestDto,
                                          seed="1234",
                                          num=2)

        # assert
        assert dto.id == "default_id"
        assert dto.name == "name1234"
        assert dto.bool_ is True
        assert dto.enum == ValueEnum.RECYCLED
        assert dto.list_of_enums == [CategoryEnum.FITNESS, CategoryEnum.FITNESS]
        assert dto.list_of_strings == ["list_of_strings12340", "list_of_strings12341"]
        assert dto.list_of_ints == [2, 3]
        assert dto.list_of_bools == [True, True]

        assert dto.date.year == 2
        assert dto.date.month == 2
        assert dto.date.day == 2
        assert dto.date.hour == 2
        assert dto.date.minute == 2
        assert dto.date.second == 2

        assert dto.list_of_dates[0].year == 2
        assert dto.list_of_dates[0].month == 2
        assert dto.list_of_dates[0].day == 2
        assert dto.list_of_dates[0].hour == 2
        assert dto.list_of_dates[0].minute == 2
        assert dto.list_of_dates[0].second == 2

        assert dto.list_of_dates[1].year == 2
        assert dto.list_of_dates[1].month == 2
        assert dto.list_of_dates[1].day == 2
        assert dto.list_of_dates[1].hour == 2
        assert dto.list_of_dates[1].minute == 2
        assert dto.list_of_dates[1].second == 2

        assert dto.decimal_num == 2.22
        assert dto.nested.id == "id1234"
        assert dto.nested.name == "name1234"

        assert dto.nested_list[0].id == "id1234"
        assert dto.nested_list[0].name == "name1234"

        assert dto.nested_list[1].id == "id1234"
        assert dto.nested_list[1].name == "name1234"


class TestJsonSnakeToCamelSerializer(TestCase):

    def setUp(self):
        self.__json_snake_to_camel_serializer = JsonSnakeToCamelSerializer()

    def test_serialize(self):
        # arrange
        input_data = TEST_DICT
        expected = TEST_DICT_JSON

        # act
        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        # assert
        assert expected == actual

    def test_serialize_nested(self):
        # arrange
        input_data = TEST_NESTED_DICT
        expected = TEST_DICT_NESTED_JSON

        # act
        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        # assert
        assert expected == actual

    def test_serialize_collection(self):
        # arrange
        input_data = TEST_LIST_SERIALIZATION
        expected = TEST_LIST_SERIALIZATION_JSON

        # act
        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        # assert
        assert expected == actual

    def test_serialize_collection_empty(self):
        # arrange
        input_data = TEST_LIST_SERIALIZATION_EMPTY
        expected = TEST_LIST_SERIALIZATION_EMPTY_JSON

        # act
        actual = self.__json_snake_to_camel_serializer.serialize(input_data)

        # assert
        assert expected == actual


class TestJsonCamelToSnakeCaseDeserializer(TestCase):

    def setUp(self):
        self.__json_camel_to_snake_case_deserializer = JsonCamelToSnakeCaseDeserializer()

    def test_deserialize(self):
        # arrange
        expected = TEST_DICT_WITH_CAPS_KEY
        input_data = TEST_DICT_JSON_WITH_CAPS_KEY

        # act
        actual = self.__json_camel_to_snake_case_deserializer.deserialize(input_data)

        # assert
        assert expected == actual

    def test_deserialize_nested(self):
        # arrange
        expected = TEST_NESTED_DICT
        input_data = TEST_DICT_NESTED_JSON

        # act
        actual = self.__json_camel_to_snake_case_deserializer.deserialize(input_data)

        # assert
        assert expected == actual

    def test_deserialize_collection(self):
        # arrange
        expected = TEST_LIST_SERIALIZATION
        input_data = TEST_LIST_SERIALIZATION_JSON

        # act
        actual = self.__json_camel_to_snake_case_deserializer.deserialize(input_data)

        # assert
        assert expected == actual

    def test_serialize_collection_empty(self):
        # arrange
        expected = TEST_LIST_SERIALIZATION_EMPTY
        input_data = TEST_LIST_SERIALIZATION_EMPTY_JSON

        # act
        actual = self.__json_camel_to_snake_case_deserializer.deserialize(input_data)

        # assert
        assert expected == actual
