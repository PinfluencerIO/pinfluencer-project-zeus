from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class CreatableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def create(self, data: T) -> bool:
        pass
