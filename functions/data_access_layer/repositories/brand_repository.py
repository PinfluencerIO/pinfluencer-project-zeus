import uuid

from functions.domain.model import Brand


class BrandRepository:
    def get(self, id_: uuid) -> Brand:
        pass

    def get_all(self) -> list[Brand]:
        pass

    def create(self, data: dict) -> Brand:
        pass

    def update(self, id_: uuid, data: dict) -> Brand:
        pass