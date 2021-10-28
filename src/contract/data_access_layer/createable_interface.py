from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.common.object_result import ObjectResult

T = TypeVar("T")


class CreatableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def create(self, data: T) -> ObjectResult[str]:
        """
        creates resource
        returns ( id of created resource, status of operation )
        """
        pass
