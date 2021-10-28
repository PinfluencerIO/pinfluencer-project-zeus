from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class DeletableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def delete(self, data: T) -> bool:
        pass
