import datetime
import inspect
import json
import random
import re
import typing
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Union

from src._types import Logger
from src.exceptions import AutoFixtureException, AutoMapperException

T = typing.TypeVar("T")


@dataclass(unsafe_hash=True)
class Rule:
    to: type = None
    _from: type = None
    field: str = None
    update: bool = False # TODO: workaround for flexi-updates
    expression: typing.Callable[[typing.Any, typing.Any], None] = None


def fullname(o):
    klass = o.__class__
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__  # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__


class PinfluencerObjectMapper:

    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__maps: list[Rule] = []

    @property
    def rules(self) -> list[Rule]:
        return self.__maps

    def add_rule(self,
                 _type_from: type,
                 _type_to: type,
                 field: str,
                 expression: typing.Callable[[typing.Any, typing.Any], None],
                 update=False):
        self.__maps.append(Rule(to=_type_to,
                                _from=_type_from,
                                field=field,
                                expression=expression,
                                update=update))

    def add_rules(self,
                  _type_from: list[type],
                  _type_to: list[type],
                  field: list[str],
                  expression: typing.Callable[[typing.Any, typing.Any], None]):
        length = len(_type_from)
        if not (length == len(_type_to) == len(field)):
            raise AutoMapperException()

        for i in range(0, length):
            _single_type_from = _type_from[i]
            _single_type_to = _type_to[i]
            single_field = field[i]

            self.add_rule(_type_from=_single_type_from,
                          _type_to=_single_type_to,
                          field=single_field,
                          expression=expression)

    def map_to_dict_and_ignore_none_fields(self, _from, to: typing.Type[T]) -> dict:
        self.__logger.log_trace(f"{vars(_from).items()}")
        mapped = self.__generic_map(_from=_from,
                                    to=to,
                                    propValues=vars(_from).items())
        new_dict = mapped.__dict__
        self.__to_dict_and_ignore_none_fields(new_dict=new_dict, mapped=mapped)
        return new_dict

    def __to_dict_and_ignore_none_fields(self, new_dict: dict, mapped):
        for property, value in list(new_dict.items()):
            try:
                if bool(typing.get_type_hints(getattr(mapped, property))):
                    self.__to_dict_and_ignore_none_fields(
                        new_dict=value,
                        mapped=getattr(mapped, property))
            except TypeError:
                self.__logger.log_trace(message=f"value {property} skipped")
            if value is None:
                new_dict.pop(property)

    def map(self, _from, to: typing.Type[T]) -> T:
        self.__logger.log_trace(f"{vars(_from).items()}")
        return self.__generic_map(_from=_from,
                                  to=to,
                                  propValues=vars(_from).items())

    def map_from_dict(self, _from, to: typing.Type[T]) -> T:
        self.__logger.log_trace(_from.items())
        return self.__generic_map(_from=_from,
                                  to=to,
                                  propValues=_from.items())

    def __generic_map(self, _from, to, propValues):
        new_dto = to()
        dict_to = all_annotations(to)
        self.__logger.log_trace("START MAPPING")
        self.__logger.log_trace(f"all annotations from DTO {dict_to}")
        self.__logger.log_trace(f"all props from _from {propValues}")
        for property, value in propValues:
            try:
                rule_match = \
                    list(filter(lambda x:
                                x._from == type(_from) and
                                x.to == to and
                                x.field == property, self.__maps))[0]
                if value is not None:
                    rule_match.expression(new_dto, _from)
            except IndexError:
                if property in dict_to:
                    setattr(new_dto, property, value)
                    if bool(typing.get_type_hints(dict_to[property])):
                        setattr(new_dto, property, self.map(_from=value, to=dict_to[property]))
        self.__logger.log_trace(f"__generic_map from {type(_from)} {to} and mapped {_from} out -> {new_dto}")
        return new_dto


class DummyLogger:

    def log_error(self, message: str):
        ...

    def log_exception(self, exception: Exception):
        ...

    def log_info(self, message: str):
        ...

    def log_debug(self, message: str):
        ...

    def log_trace(self, message: str):
        ...


# TODO
class ConsoleLogger:

    def __log(self, _type: str, message: str):
        _function = inspect.stack()[2].function
        _class = "None"
        _module = "Unknown"
        try:
            _class = type(inspect.stack()[2].frame.f_locals['self']).__name__
            _module = type(inspect.stack()[2].frame.f_locals['self']).__module__
        except:
            ...
        name = f"{_module}.{_class}.{_function}"
        print(f"{_type}: {name}: {message}")

    def log_error(self, message: str):
        self.__log(_type="ERROR", message=message)

    def log_exception(self, exception: Exception):
        self.__log(_type="ERROR", message=f"EXCEPTION: {str(exception)}")

    def log_info(self, message: str):
        self.__log(_type="INFO", message=message)

    def log_debug(self, message: str):
        self.__log(_type="DEBUG", message=message)

    def log_trace(self, message: str):
        self.__log(_type="TRACE", message=message)


class FlexiUpdater:

    def __init__(self, mapper: PinfluencerObjectMapper):
        self.__mapper = mapper

    def update(self, request, object_to_update):
        values = list(vars(object_to_update).items())
        for key, value in values:
            try:
                try:
                    matching_rule = list(filter(lambda x:
                                                x._from == type(request) and
                                                x.to == type(object_to_update) and
                                                x.field == key, self.__mapper.rules))[0]

                    try:
                        value_in_request = getattr(request, key)
                        if value_in_request is not None:
                            matching_rule.expression(object_to_update, request)
                    except AttributeError:
                        matching_rule.expression(object_to_update, request)
                except IndexError:
                    value_in_request = getattr(request, key)
                    if value_in_request is not None:
                        setattr(object_to_update, key, getattr(request, key))
            except AttributeError:
                ...


class AutoFixture:

    def create_many_dict(self, dto,
                         ammount,
                         seed=None,
                         num=None,
                         nest=0,
                         list_limit=100):
        many = self.create_many(dto=dto,
                                ammount=ammount,
                                seed=seed,
                                num=num,
                                nest=nest,
                                list_limit=list_limit)
        return list(map(lambda x: x.__dict__, many))

    def create_dict(self, dto,
                    seed=None,
                    num=None,
                    nest=0,
                    list_limit=100):
        return self.create(dto=dto,
                           seed=seed,
                           num=num,
                           nest=nest,
                           list_limit=list_limit).__dict__

    def create_many(self, dto,
                    ammount,
                    seed=None,
                    num=None,
                    nest=0,
                    list_limit=100):
        list_of_dtos = []
        for i in range(0, ammount):
            list_of_dtos.append(self.create(dto=dto,
                                            seed=seed,
                                            num=num,
                                            nest=nest,
                                            list_limit=list_limit))
        return list_of_dtos

    def create(self, dto: typing.Type[T],
               seed=None,
               num=None,
               nest=0,
               list_limit=100) -> T:
        self.__validate_predictable_data(num, seed)

        try:
            new_value = dto()
        except TypeError:
            raise AutoFixtureException("class must empty ctor, if a dataclass, must have fields initialised to "
                                       "sensible defaults or None")

        is_predictable_data = seed is not None and num is not None

        members = all_annotations(cls=dto).items()
        for (key, _type) in members:

            if (getattr(new_value, key) is None) or (
                    typing.get_origin(_type) is list and getattr(new_value, key) == []):

                if _type is str:
                    self.__generate_string_field(is_predictable_data, key, new_value, seed)

                if _type is bool:
                    self.__generate_bool_field(is_predictable_data, key, new_value, num)

                if _type == datetime.datetime:
                    self.__generate_datetime_field(is_predictable_data, key, new_value, num)

                if _type is int:
                    self.__generate_int_field(is_predictable_data, key, new_value, num)

                if _type is float:
                    self.__generate_float_field(is_predictable_data, key, new_value, num)

                if _type == list[str]:
                    self.__generate_str_list_field(is_predictable_data, key, new_value, num, seed, list_limit)

                if _type == list[int]:
                    self.__generate_int_list_field(is_predictable_data, key, new_value, num, list_limit)

                if _type == list[bool]:
                    self.__generate_bool_list_field(is_predictable_data, key, new_value, num, list_limit)

                if _type == list[datetime.datetime]:
                    self.__generate_datetime_list_field(is_predictable_data, key, new_value, num, list_limit)

                if _type == list[float]:
                    self.__generate_float_list_field(is_predictable_data, key, new_value, num, list_limit)

                if type(_type) is type(Enum):
                    self.__generate_random_enum_field(_type, is_predictable_data, key, new_value, num)

                if bool(typing.get_type_hints(_type)):
                    self.__generate_class_field(_type, key, nest, new_value, num, seed)

                if typing.get_origin(_type) is list:
                    arg = typing.get_args(_type)[0]
                    if type(arg) is type(Enum):
                        self.__generate_list_of_enums_field(arg, is_predictable_data, key, new_value, num, list_limit)
                    if bool(typing.get_type_hints(arg)):
                        self.__generate_class_list(arg, is_predictable_data, key, nest, new_value, num, seed,
                                                   list_limit)

        return new_value

    def __generate_class_field(self, _type, key, nest, new_value, num, seed):
        setattr(new_value, key, self.create(dto=_type,
                                            seed=seed,
                                            num=num,
                                            nest=nest + 1))

    def __generate_class_list(self, _type, is_predictable_data, key, nest, new_value, num, seed, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                value_for_given_member.append(self.create(dto=_type,
                                                          seed=seed,
                                                          num=num,
                                                          nest=nest + 1))
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(self.create(dto=_type,
                                                          seed=seed,
                                                          num=num,
                                                          nest=nest + 1))
        setattr(new_value, key, value_for_given_member)

    def __generate_list_of_enums_field(self, _type, is_predictable_data, key, new_value, num, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                enum_iterable = list(_type)
                length = len(enum_iterable)
                index = num % length
                value_for_given_member.append(enum_iterable[index])
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(random.choice(list(_type)))
        setattr(new_value, key, value_for_given_member)

    def __generate_random_enum_field(self, _type, is_predictable_data, key, new_value, num):
        if is_predictable_data:
            enum_iterable = list(_type)
            length = len(enum_iterable)
            index = num % length
            value_for_given_member = enum_iterable[index]
        else:
            value_for_given_member = random.choice(list(_type))
        setattr(new_value, key, value_for_given_member)

    def __generate_datetime_list_field(self, is_predictable_data, key, new_value, num, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                value_for_given_member.append(datetime.datetime(2, 2, 2, 2, 2, 2))
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(datetime.datetime.utcnow())
        setattr(new_value, key, value_for_given_member)

    def __generate_bool_list_field(self, is_predictable_data, key, new_value, num, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                value_for_given_member.append(bool(num))
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(random.choice([True, False]))
        setattr(new_value, key, value_for_given_member)

    def __generate_datetime_field(self, is_predictable_data, key, new_value, num):
        if is_predictable_data:
            value_for_given_member = datetime.datetime(num, num, num, num, num, num)
        else:
            value_for_given_member = datetime.datetime.utcnow()
        setattr(new_value, key, value_for_given_member)

    def __generate_bool_field(self, is_predictable_data, key, new_value, num):
        if is_predictable_data:
            value_for_given_member = bool(num)
        else:
            value_for_given_member = random.choice([True, False])
        setattr(new_value, key, value_for_given_member)

    @staticmethod
    def __generate_float_list_field(is_predictable_data, key, new_value, num, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                trailing_decimals = ""
                for i in range(0, num):
                    trailing_decimals = f"{trailing_decimals}{num}"
                value_for_given_member_item = float(f"{num}.{trailing_decimals}")
                value_for_given_member.append(value_for_given_member_item)
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(random.uniform(0, 100))
        setattr(new_value, key, value_for_given_member)

    @staticmethod
    def __generate_int_list_field(is_predictable_data, key, new_value, num, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                value_for_given_member.append(num + i)
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member.append(random.randint(0, 100))
        setattr(new_value, key, value_for_given_member)

    def __generate_str_list_field(self, is_predictable_data, key, new_value, num, seed, list_limit):
        if is_predictable_data:
            value_for_given_member = []
            for i in range(0, num):
                value_for_given_member_item = key
                value_for_given_member_item = f"{value_for_given_member_item}{seed}{i}"
                value_for_given_member.append(value_for_given_member_item)
        else:
            value_for_given_member = []
            for i in range(0, random.randint(0, list_limit)):
                value_for_given_member_item = key
                value_for_given_member_item = f"{value_for_given_member_item}{self.__generate_random_seed()}"
                value_for_given_member.append(value_for_given_member_item)
        setattr(new_value, key, value_for_given_member)

    @staticmethod
    def __generate_random_seed() -> str:
        return str(uuid.uuid4()).split("-")[0]

    @staticmethod
    def __validate_predictable_data(num, seed):
        if seed is not None and num is None:
            raise AutoFixtureException("seed and num must be both set to create predictable data")
        if seed is not None and num is None:
            raise AutoFixtureException("seed and num must be both set to create predictable data")

    @staticmethod
    def __generate_float_field(is_predictable_data, key, new_value, num):
        if is_predictable_data:
            trailing_decimals = ""
            for i in range(0, num):
                trailing_decimals = f"{trailing_decimals}{num}"
            value_for_given_member = float(f"{num}.{trailing_decimals}")
        else:
            value_for_given_member = random.uniform(0, 100)
        setattr(new_value, key, value_for_given_member)

    @staticmethod
    def __generate_int_field(is_predictable_data, key, new_value, num):
        if is_predictable_data:
            value_for_given_member = num
        else:
            value_for_given_member = random.randint(0, 100)
        setattr(new_value, key, value_for_given_member)

    def __generate_string_field(self, is_predictable_data, key, new_value, seed):
        value_for_given_member = key
        if is_predictable_data:
            value_for_given_member = f'{value_for_given_member}{seed}'
        else:
            value_for_given_member = f'{value_for_given_member}{self.__generate_random_seed()}'
        setattr(new_value, key, value_for_given_member)


def all_annotations(cls):
    d = {}
    for c in cls.mro():
        try:
            d.update(**c.__annotations__)
        except AttributeError:
            # object, at least, has no __annotations__ attribute.
            pass
    return d


class JsonSnakeToCamelSerializer:

    def serialize(self, data: Union[dict, list]) -> str:
        return json.dumps(self.__snake_case_to_camel_case_dict(d=data), default=str)

    def __snake_case_to_camel_case_dict(self, d):
        if isinstance(d, list):
            return [self.__snake_case_to_camel_case_dict(i) if isinstance(i, (dict, list)) else i for i in d]
        return {self.__snake_case_key_to_camel_case(a): self.__snake_case_to_camel_case_dict(b) if isinstance(b, (
            dict, list)) else b for a, b in d.items()}

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
        return {self.__camel_case_key_to_snake_case(a): self.__camel_case_to_snake_case_dict(b) if isinstance(b, (
            dict, list)) else b for a, b in d.items()}

    @staticmethod
    def __camel_case_key_to_snake_case(key: str) -> str:
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', key)
        return '_'.join(map(str.lower, words))


def valid_uuid(id_, logger: Logger):
    try:
        val = uuid.UUID(id_, version=4)
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            logger.log_error(f'equality failed {val} {id_}')
    except ValueError as ve:
        logger.log_exception(ve)
    except AttributeError as e:
        logger.log_exception(e)

    return False
