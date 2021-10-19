import datetime
import uuid


class Brand:

    def __init__(self, id_: uuid, created: datetime, name: str, bio: str, website:str, email:str, version: int = 0):
        self.id_ = id_
        self.created = created
        self.name = name
        self.bio = bio
        self.website = website
        self.email = email
        self.version = version


class Product:

    def __init__(self, id_: uuid, created: datetime, name: str, description: str, image: str, version: int = 0):
        self.id_ = id_
        self.created = created
        self.name = name
        self.description = description
        self.image = image
        self.version = version
