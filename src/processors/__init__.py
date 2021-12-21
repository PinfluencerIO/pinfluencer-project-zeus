import uuid

import boto3

from src import log_util
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product

BUCKET = 'pinfluencer-product-images'

s3 = boto3.client('s3')


def get_cognito_user(event):
    return event['requestContext']['authorizer']['jwt']['claims']['cognito:username']


def protect_email_from_update_if_held_in_claims(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        print(f"Found email in claim: {event['requestContext']['authorizer']['jwt']['claims']['email']}")
        print(f'before {body}')
        body['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
        print(f'after {body}')


def valid_path_resource_id(event, resource_key):
    try:
        id_ = event['pathParameters'][resource_key]
        if valid_uuid(id_):
            return id_
        else:
            print(f'Path parameter not a valid uuid {id_}')
    except KeyError:
        print(f'Missing key in event pathParameters.{resource_key}')

    return None


def valid_uuid(id_):
    try:
        val = uuid.UUID(id_, version=4)
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            log_util.print_exception(f'equality failed {val} {id_}')
    except ValueError as ve:
        log_util.print_exception(ve)
    except AttributeError as e:
        log_util.print_exception(e)

    return False


# TODO Add test for schemas
def get_image_update_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "image_bytes": {
                    "type": "string"
                }
            },
        "required": ["image_bytes"]
    }
    return schema


def get_product_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "requirements": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "image_bytes": {
                    "type": "string"
                }
            },
        "required": ["name", "description", "requirements", "image_bytes"]
    }
    return schema


def get_product_update_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "requirements": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                }
            },
        "required": ["name", "description", "requirements"]
    }
    return schema


def get_brand_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "website": {
                    "type": "string",
                    "pattern": r"^(https?\:\/\/)?([\da-zA-Z\.-]+)\.([a-z\.]{2,6})(\/[\w]*)*$"
                },
                "email": {
                    "type": "string",
                    "pattern": r"^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
                },
                "instahandle": {
                    "type": "string",
                    "pattern": "^.{1,30}$"
                },
                "image_bytes": {
                    "type": "string"
                }
            },
        "required": ["name", "description", "website", "email", "image_bytes"]
    }
    return schema


def update_brand_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "website": {
                    "type": "string",
                    "pattern": r"^(https?\:\/\/)?([\da-zA-Z\.-]+)\.([a-z\.]{2,6})(\/[\w]*)*$"
                },
                "email": {
                    "type": "string",
                    "pattern": r"^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
                },
                "instahandle": {
                    "type": "string",
                    "pattern": "^.{1,30}$"
                }
            },
        "required": ["name", "description", "website", "email"]
    }
    return schema


types = {
    'brand': {
        'key': 'brand_id',
        'type': Brand,
        'post': {
            'validator': get_brand_payload_schema()
        },
        'put': {
            'validator': update_brand_payload_schema()
        },
        'patch': {
            'validator': get_image_update_payload_schema()
        }
    },
    'product': {
        'key': 'product_id',
        'type': Product,
        'post': {
            'validator': get_product_payload_schema()
        },
        'put': {
            'validator': get_product_update_payload_schema()
        },
        'patch': {
            'validator': get_image_update_payload_schema()
        }
    }
}
