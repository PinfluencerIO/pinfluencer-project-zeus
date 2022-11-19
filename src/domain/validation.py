import validators
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

# TODO: do actual validation and write tests for it

common_user_schema = {
    "email": {
        "type": "string",
        "pattern": r"^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
    },
}

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
                "pattern": "^[\s\S]{1,500}$"
            },
            "insta_handle": {
                "type": "string",
                "pattern": "^.{1,30}$"
            }
        },
    "required": []
}

influencer_payload_schema = {
    "type": "object",
    "properties":
        {
            "bio": {
                "type": "string",
                "pattern": "^[\s\S]{1,500}$"
            },
            "insta_handle": {
                "type": "string",
                "pattern": "^.{1,30}$"
            }
        },
    "required": []
}

listing_payload_schema = {
    "type": "object",
    "properties":
        {
            "title": {
                "type": "string",
                "pattern": "^.{1,120}$"
            }
        },
    "required": []
}


class ListingValidator:

    def validate_listing(self, payload):
        validate(instance=payload, schema=listing_payload_schema)


class BaseValidator:
    def _common_user_validate(self, payload, schema_input):
        schema = schema_input
        schema['properties'].update(common_user_schema)
        if 'website' in payload:
            website = payload['website']
            if not validators.url(website):
                raise ValidationError("email invalid")
        validate(instance=payload, schema=schema)


class BrandValidator(BaseValidator):

    def validate_brand(self, payload):
        self._common_user_validate(payload=payload, schema_input=brand_payload_schema)


class InfluencerValidator(BaseValidator):

    def validate_influencer(self, payload):
        self._common_user_validate(payload=payload, schema_input=influencer_payload_schema)
