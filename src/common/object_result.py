from typing import TypeVar, Generic

from src.common.result import Result

T = TypeVar("T")


class ObjectResult(Generic[T], Result):
    value: T
