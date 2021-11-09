import abc
import base64
import io
import uuid

import boto3
from filetype import filetype

from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.http_util import PinfluencerResponse

BUCKET = 'pinfluencer-product-images'

s3 = boto3.client('s3')


# Todo: Not sure this is the right place for an interface...read up about it.
class ProcessInterface(abc.ABC):
    _data_manager: DataManagerInterface

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    @abc.abstractmethod
    def do_process(self, event: dict) -> PinfluencerResponse:
        pass


def get_user(event):
    return event['requestContext']['authorizer']['jwt']['claims']['cognito:username']


def upload_image_to_s3(path: str, image_base64_encoded: str) -> str:
    image = base64.b64decode(image_base64_encoded)
    f = io.BytesIO(image)
    file_type = filetype.guess(f)
    if file_type is not None:
        mime = file_type.MIME
    else:
        mime = 'image/jpg'
    image_id = str(uuid.uuid4())
    file = f'{image_id}.{file_type.EXTENSION}'
    key = f'{path}/{file}'
    s3.put_object(Bucket=BUCKET,
                  Key=key, Body=image,
                  ContentType=mime,
                  Tagging='public=yes')
    return file


def delete_image_from_s3(path: str) -> None:
    s3.delete_object(Bucket=BUCKET, Key=path)
