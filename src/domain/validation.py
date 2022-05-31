from jsonschema.validators import validate

brand_payload_schema = {
    "type": "object",
    "properties":
        {
            "brand_name": {
                "type": "string",
                "pattern": "^.{1,120}$"
            },
            "brand_description": {
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
            "insta_handle": {
                "type": "string",
                "pattern": "^.{1,30}$"
            }
        },
    "required": ["brand_name", "brand_description", "website", "email"]
}


class BrandValidator:

    def validate_brand(self, payload):
        validate(instance=payload, schema=brand_payload_schema)
