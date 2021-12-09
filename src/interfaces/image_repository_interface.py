from abc import ABC, abstractmethod


class ImageRepositoryInterface(ABC):

    @abstractmethod
    def upload(self, path: str, image_base64_encoded: str) -> str:
        pass

    @abstractmethod
    def retrieve(self, path: str) -> str:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        pass
