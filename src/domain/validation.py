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