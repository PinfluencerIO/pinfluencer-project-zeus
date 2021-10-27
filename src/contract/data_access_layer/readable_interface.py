from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class ReadableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def read(self, id: str) -> T:
        pass
