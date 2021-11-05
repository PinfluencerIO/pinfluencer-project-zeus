from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class DataManagerInterface(ABC):

    @property
    @abstractmethod
    def engine(self) -> Engine:
        pass

    @property
    @abstractmethod
    def session(self) -> Session:
        pass
