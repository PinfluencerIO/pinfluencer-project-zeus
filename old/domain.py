import abc
import uuid


class RepositoryInterface:
    @abc.abstractmethod
    def get(self, id_: uuid):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass

    @abc.abstractmethod
    def find_by(self, where):
        pass

    @abc.abstractmethod
    def create(self, data: dict):
        pass

    @abc.abstractmethod
    def update(self, id_: uuid, data: dict):
        pass

    @abc.abstractmethod
    def delete(self, id_):
        pass
