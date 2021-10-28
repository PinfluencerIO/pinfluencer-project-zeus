from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.result import Result

T = TypeVar("T")


class UpdatableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def update(self, data: T) -> Result:
        """
        updates single resource
        returns ( operation result )
        """
        pass
