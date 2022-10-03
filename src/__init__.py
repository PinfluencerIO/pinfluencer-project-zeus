from typing import TypeVar, Type

from simple_injection import ServiceCollection


T = TypeVar("T")


class ServiceLocator:

    def __init__(self, ioc: ServiceCollection):
        self.__ioc = ioc

    def locate(self, service: Type[T]) -> T:
        return self.__ioc.resolve(service)