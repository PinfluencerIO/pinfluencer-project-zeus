from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.result import Result

T = TypeVar("T")


class DeletableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def delete(self, id: str) -> Result:
        """
        deletes resource
        returns ( status of operation )
        """
        pass
