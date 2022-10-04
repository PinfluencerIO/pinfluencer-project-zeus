from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union, OrderedDict, Callable, Protocol

from src._types import Serializer, Logger
from src.crosscutting import valid_uuid

SUBSEQUENCE = "subsequence"

COMMAND = "command"

BRAND_ID_PATH_KEY = 'brand_id'
INFLUENCER_ID_PATH_KEY = 'influencer_id'


@dataclass
class PinfluencerRequest:
    body: dict
    id: str = ""
    auth_user_id: str = ""


@dataclass(unsafe_hash=True)
class ErrorCapsule:
    message: str = "something went wrong",
    status: int = 500


class PinfluencerResponse:
    def __init__(self, status_code: int = 200, body: Union[dict, list] = {}) -> None:
        self.status_code = status_code
        self.body = body

    def is_ok(self):
        return 200 <= self.status_code < 300

    def as_json(self, serializer: Serializer) -> dict:
        return {
            "statusCode": self.status_code,
            "body": serializer.serialize(self.body),
            "headers": {"Content-Type": "application/json",
                        'Access-Control-Allow-Origin': "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"},
        }

    @staticmethod
    def as_500_error(message="unexpected server error, please try later :("):
        return PinfluencerResponse(500, {"message": message})

    @staticmethod
    def as_400_error(message='client error, please check request.'):
        return PinfluencerResponse(400, {"message": message})


def get_cognito_user(event):
    return event['requestContext']['authorizer']['jwt']['claims']['cognito:username']




@dataclass(unsafe_hash=True)
class PinfluencerContext:
    response: PinfluencerResponse = None,
    short_circuit: bool = False,
    route_key: str = "",
    event: Union[list, dict] = field(default_factory=dict),
    auth_user_id: str = "",
    body: dict = field(default_factory=dict)
    id: str = ""
    error_capsule: list[ErrorCapsule] = field(default_factory=list)
    cached_values: OrderedDict = field(default_factory=dict)


PinfluencerCommand = Callable[[PinfluencerContext], None]

class PinfluencerSequenceBuilder(Protocol):

    def generate_sequence(self) -> list[PinfluencerCommand]:
        ...

    def build(self):
        ...


@dataclass
class Route:
    sequence_builder: PinfluencerSequenceBuilder


def valid_path_resource_id(event, resource_key, logger: Logger):
    try:
        id_ = event['pathParameters'][resource_key]
        if valid_uuid(id_, logger=logger):
            return id_
        else:
            logger.log_error(f'Path parameter not a valid uuid {id_}')
    except KeyError:
        logger.log_error(f'Missing key in event pathParameters.{resource_key}')
    return None


PinfluencerSequenceComponent = Union[PinfluencerCommand, PinfluencerSequenceBuilder]


class FluentSequenceBuilder(ABC):

    def __init__(self):
        self.__components: list[(str, PinfluencerSequenceComponent)] = []

    def _add_command(self, command: PinfluencerCommand) -> 'FluentSequenceBuilder':
        self.__components.append((COMMAND, command))
        return self

    def _add_sequence_builder(self, sequence_builder: PinfluencerSequenceBuilder) -> 'FluentSequenceBuilder':
        self.__components.append((SUBSEQUENCE, sequence_builder))
        return self

    def generate_sequence(self) -> list[PinfluencerCommand]:
        self.build()
        new_list = []
        for (name, component) in self.__components:
            if name == COMMAND:
                new_list.append(component)
            if name == SUBSEQUENCE:
                sequence_component: PinfluencerSequenceBuilder = component
                commands = sequence_component.generate_sequence()
                new_list.extend(commands)
        return new_list

    @abstractmethod
    def build(self):
        ...

    @property
    def components(self) -> list[PinfluencerSequenceComponent]:
        return list(map(lambda x: x[1], self.__components))
