from abc import ABC

from src.domain.services import Container


class BaseProcessor(ABC):
    _container: Container

    def __init__(self):
        self._container = Container()