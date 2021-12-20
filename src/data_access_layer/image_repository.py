import base64
import io
import json
import uuid

import boto3
from botocore.client import BaseClient
from filetype import filetype


class S3ImageRepository:
    __bucket_name: str
    __s3_client: BaseClient

    def __init__(self):
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path: str, image_base64_encoded: str) -> str:
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
        self.__s3_client.put_object(Bucket=self.__bucket_name,
                                    Key=key, Body=image,
                                    ContentType=mime,
                                    Tagging='public=yes')
        return file

    def delete(self, path: str) -> None:
        self.__s3_client.delete_object(Bucket=self.__bucket_name, Key=path)

    def retrieve(self, path: str) -> str:
        image_object = self.__s3_client.get_object(self.__bucket_name, path)
        return json.loads(image_object['Body'].read())
