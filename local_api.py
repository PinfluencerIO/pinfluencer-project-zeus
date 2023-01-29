import json
import os
from dataclasses import dataclass

from flask import Flask, request, Response

from src.app import lambda_handler, logger_factory
from src.crosscutting import PinfluencerObjectMapper

os.environ["ENVIRONMENT"] = "DEV"

if "AWS_DEFAULT_REGION" not in os.environ: logger_factory().log_error("environment var AWS_DEFAULT_REGION is not set")
if "DB_USER" not in os.environ: logger_factory().log_error("environment var DB_USER is not set")
if "DB_PASSWORD" not in os.environ: logger_factory().log_error("environment var DB_PASSWORD is not set")
if "DB_NAME" not in os.environ: logger_factory().log_error("environment var DB_NAME is not set")
if "DB_URL" not in os.environ: logger_factory().log_error("environment var DB_URL is not set")
if "USER_POOL_ID" not in os.environ: logger_factory().log_error("environment var USER_POOL_ID is not set")

app = Flask(__name__)


@dataclass(unsafe_hash=True)
class PinfResponse:
    body: str = None
    headers: dict = None

    # Violates naming but this is only for local testing so dw about it
    statusCode: int = None


@app.route("/brands/me/images/<image>", methods=['POST'])
def update_brand_logo(image):
    return generic_handler(routeKey="POST /brands/me/images/{image_field}",
                           params={
                               "image_field": image
                           })


@app.route("/brands/me", methods=['GET'])
def get_brand_for_auth_user():
    return generic_handler(routeKey="GET /brands/me", params={})


@app.route("/brands/me", methods=['POST'])
def create_brand_for_auth_user():
    return generic_handler(routeKey="POST /brands/me", params={})


@app.route("/brands/me", methods=['PATCH'])
def update_brand_for_auth_user():
    return generic_handler(routeKey="PATCH /brands/me", params={})


@app.route("/brands", methods=['GET'])
def get_all_brands():
    return generic_handler(routeKey="GET /brands", params={})


@app.route("/brands/<id>", methods=['GET'])
def get_brand_by_id(id):
    return generic_handler(routeKey="GET /brands/{brand_id}", params={"brand_id": id})


@app.route("/influencers/me/images/<image>", methods=['POST'])
def update_influencer_logo(image):
    return generic_handler(routeKey="POST /influencers/me/images/{image_field}",
                           params={
                               "image_field": image
                           })


@app.route("/influencers/me", methods=['GET'])
def get_influencer_for_auth_user():
    return generic_handler(routeKey="GET /influencers/me", params={})


@app.route("/influencers/me", methods=['POST'])
def create_influencer_for_auth_user():
    return generic_handler(routeKey="POST /influencers/me", params={})


@app.route("/influencers/me", methods=['PATCH'])
def update_influencer_for_auth_user():
    return generic_handler(routeKey="PATCH /influencers/me", params={})


@app.route("/influencers", methods=['GET'])
def get_all_influencers():
    return generic_handler(routeKey="GET /influencers", params={})


@app.route("/influencers/<id>", methods=['GET'])
def get_influencer_by_id(id):
    return generic_handler(routeKey="GET /influencers/{influencer_id}", params={"influencer_id": id})


@app.route("/brands/me/listings", methods=['GET'])
def get_list_of_listings_for_brand():
    return generic_handler(routeKey="GET /brands/me/listings", params={})


@app.route("/influencers/me/listings", methods=['GET'])
def get_list_of_listings_for_influencer():
    return generic_handler(routeKey="GET /influencer/me/listings", params={})


@app.route("/brands/me/listings", methods=['POST'])
def create_listing_for_brand():
    return generic_handler(routeKey="POST /brands/me/listings", params={})


@app.route("/brands/me/listings/<id>", methods=['PATCH'])
def update_listing(id):
    return generic_handler(routeKey="PATCH /brands/me/listings/{listing_id}", params={"listing_id": id})


@app.route("/brands/me/listings/<id>/images/<image>", methods=['POST'])
def update_listing_image(id, image):
    return generic_handler(routeKey="POST /brands/me/listings/{listing_id}/images/{image_field}", params={
        "listing_id": id,
        "image_field": image
    })


@app.route("/listings/<id>", methods=['GET'])
def get_listing_by_id(id):
    return generic_handler(routeKey="GET /listings/{listing_id}", params={"listing_id": id})


@app.route("/users/me/notifications", methods=['POST'])
def create_notification_for_auth_user():
    return generic_handler(routeKey="POST /users/me/notifications", params={})


@app.route("/notifications/<id>", methods=['GET'])
def get_notification_by_id(id):
    return generic_handler(routeKey="GET /notifications/{notification_id}", params={'notification_id': id})


@app.route("/influencers/me/audience-age-splits", methods=['POST'])
def create_audience_age_splits():
    return generic_handler(routeKey="POST /influencers/me/audience-age-splits", params={})

@app.route("/influencers/me/audience-age-splits", methods=['GET'])
def get_audience_age_splits():
    return generic_handler(routeKey="GET /influencers/me/audience-age-splits", params={})

@app.route("/influencers/me/audience-age-splits", methods=['PATCH'])
def update_audience_age_splits():
    return generic_handler(routeKey="PATCH /influencers/me/audience-age-splits", params={})

@app.route("/influencers/me/audience-gender-splits", methods=['POST'])
def create_audience_gender_splits():
    return generic_handler(routeKey="POST /influencers/me/audience-gender-splits", params={})

@app.route("/influencers/me/audience-gender-splits", methods=['GET'])
def get_audience_gender_splits():
    return generic_handler(routeKey="GET /influencers/me/audience-gender-splits", params={})

@app.route("/influencers/me/audience-gender-splits", methods=['PATCH'])
def update_audience_gender_splits():
    return generic_handler(routeKey="PATCH /influencers/me/audience-gender-splits", params={})


@app.route("/influencer-profile", methods=['POST'])
def create_influencer_profile():
    return generic_handler(routeKey="POST /influencer-profile", params={})

@app.route("/influencers/me/collaborations", methods=['POST'])
def create_collaboration():
    return generic_handler(routeKey="POST /influencers/me/collaborations", params={})

@app.route("/influencer-profile", methods=['GET'])
def get_influencer_profile():
    return generic_handler(routeKey="GET /influencer-profile", params={})

@app.route("/influencer-profile", methods=['PATCH'])
def update_influencer_profile():
    return generic_handler(routeKey="PATCH /influencer-profile", params={})

def generic_handler(routeKey: str, params: dict):
    body_string = None
    try:
        body = request.json
        body_string = json.dumps(body)
    except Exception:
        ...
    if body_string is None:
        body_string = ""

    auth_user = request.headers["Authorization"].split(" ")[1]
    response = lambda_handler(event={
        "body": body_string,
        'requestContext': {
            'authorizer': {
                'jwt': {
                    'claims': {
                        'username': auth_user
                    }
                }
            }
        },
        "routeKey": routeKey,
        "pathParameters": params
    }, context={})
    response_object: PinfResponse = PinfluencerObjectMapper(logger=logger_factory()).map_from_dict(_from=response,
                                                                                                   to=PinfResponse)
    return Response(response_object.body,
                    status=response_object.statusCode,
                    mimetype='application/json')
