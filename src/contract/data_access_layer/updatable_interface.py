from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class UpdatableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def update(self, data: T) -> bool:
        pass
