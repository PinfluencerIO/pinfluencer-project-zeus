import abc
import uuid
from typing import TypeVar, Generic

from functions.domain.model import Brand, Product

T = TypeVar('T', Brand, Product)


# Todo: This has to go! Replace with a professional ORM library
class RepositoryInterface(Generic[T]):
    @abc.abstractmethod
    def get(self, id_: uuid) -> T:
        pass

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abc.abstractmethod
    def find_by(self, column, value) -> T:
        pass

    @abc.abstractmethod
    def create(self, data: dict) -> T:
        pass

    @abc.abstractmethod
    def update(self, id_: uuid, data: dict) -> T:
        pass

    @abc.abstractmethod
    def delete(self, id_) -> bool:
        pass
