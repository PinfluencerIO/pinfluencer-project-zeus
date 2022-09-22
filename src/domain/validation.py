from jsonschema.validators import validate

# TODO: do actual validation and write tests for it

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


class BrandValidator:

    def validate_brand(self, payload):
        validate(instance=payload, schema=brand_payload_schema)


class InfluencerValidator:

    def validate_influencer(self, payload):
        validate(instance=payload, schema=influencer_payload_schema)
