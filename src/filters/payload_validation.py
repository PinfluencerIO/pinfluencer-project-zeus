import json

from jsonschema import validate

from src.filters import FilterInterface, FilterResponse


class BrandPutPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        try:
            validate(instance=payload, schema=update_brand_payload_schema())
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating BrandPutPayload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


class BrandImagePatchPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        try:
            validate(instance=payload, schema=get_image_update_payload_schema())
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating ImagePatchPayload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


class BrandPostPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_brand_payload_schema()))
            if len(payload['email']) > 120:
                print(f'email is longer than column size, clipping ')
                payload['email'] = payload['email'][:120]
            if len(payload['website']) > 120:
                print(f'website is longer than column size, clipping ')
                payload['website'] = payload['website'][:120]
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating brand payload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


class ProductPostPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_product_payload_schema()))
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating product payload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


class ProductPutPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_product_update_payload_schema()))
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating product update payload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


class ProductImagePatchPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_image_update_payload_schema()))
            return FilterResponse('', 200, {})
        except Exception as e:
            print(f'Validating product update payload failed {e}')
            return FilterResponse('Invalid payload', 400, {})


def get_image_update_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "image": {
                    "type": "string"
                }
            },
        "required": ["image"]
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
                "image": {
                    "type": "string"
                }
            },
        "required": ["name", "description", "requirements", "image"]
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
                    "pattern": "^(https?\:\/\/)?([\da-zA-Z\.-]+)\.([a-z\.]{2,6})(\/[\w]*)*$"
                },
                "email": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
                },
                "instahandle": {
                    "type": "string",
                    "pattern": "^.{1,30}$"
                },
                "image": {
                    "type": "string"
                }
            },
        "required": ["name", "description", "website", "email", "image"]
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
                    "pattern": "^(https?\:\/\/)?([\da-zA-Z\.-]+)\.([a-z\.]{2,6})(\/[\w]*)*$"
                },
                "email": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
                },
                "instahandle": {
                    "type": "string",
                    "pattern": "^.{1,30}$"
                }
            },
        "required": ["name", "description", "website", "instahandle", "email"]
    }
    return schema
