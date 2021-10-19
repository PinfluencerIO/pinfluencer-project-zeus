import datetime
import json
import uuid

from attr import dataclass


class Brand:
    id_: uuid
    created: datetime
    name: str
    bio: str
    website: str
    email: str
    version: int

    def as_json(self):
        return json.dumps(self.__dict__, default=str)


@dataclass()
class Product:
    id_: uuid
    created: datetime
    name: str
    description: str
    image: str
    version: int

    def as_json(self):
        return json.dumps(self.__dict__, default=str)

# example Product
# p = Product(id_=uuid.uuid4(),
#             created=datetime.datetime.now(),
#             name='Product Name',
#             description='product description',
#             image='key to image in s3',
#             version=1)
