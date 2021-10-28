from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class ReadableInterface(Generic[T], metaclass=ABC):

    @abstractmethod
    def read(self, id: str) -> T:
        """
        reads single resource
        returns ( resource )
        """
        pass

    @abstractmethod
    def readall(self) -> list[T]:
        """
        reads all resources
        returns ( list of resources )
        """
        pass
