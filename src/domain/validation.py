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

campaign_payload_schema = {
    "type": "object",
    "properties":
        {
            "campaign_hashtag": {
                "type": "string",
                "pattern": "^.{1,120}$"
            }
        },
    "required": []
}


class CampaignValidator:

    def validate_campaign(self, payload):
        validate(instance=payload, schema=campaign_payload_schema)


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
