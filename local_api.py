import json
import os
from dataclasses import dataclass

from flask import Flask, request, Response

from src.app import lambda_handler, logger_factory
from src.crosscutting import PinfluencerObjectMapper

os.environ["ENVIRONMENT"] = "DEV"

if "AWS_DEFAULT_REGION" not in os.environ: logger_factory().log_error("environment var AWS_DEFAULT_REGION is not set")
if "AWS_SAM_STACK_NAME" not in os.environ: logger_factory().log_error("environment var AWS_SAM_STACK_NAME is not set")
if "DB_USER" not in os.environ: logger_factory().log_error("environment var DB_USER is not set")
if "DB_PASSWORD" not in os.environ: logger_factory().log_error("environment var DB_PASSWORD is not set")
if "DB_CLUSTER_ARN" not in os.environ: logger_factory().log_error("environment var DB_CLUSTER_ARN is not set")
if "DB_SECRET_ARN" not in os.environ: logger_factory().log_error("environment var DB_SECRET_ARN is not set")
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


@app.route("/brands/me/campaigns", methods=['GET'])
def get_list_of_campaigns_for_brand():
    return generic_handler(routeKey="GET /brands/me/campaigns", params={})


@app.route("/brands/me/campaigns", methods=['POST'])
def create_campaign_for_brand():
    return generic_handler(routeKey="POST /brands/me/campaigns", params={})


@app.route("/brands/me/campaigns/<id>", methods=['PATCH'])
def update_campaign(id):
    return generic_handler(routeKey="PATCH /brands/me/campaigns/{campaign_id}", params={"campaign_id": id})


@app.route("/brands/me/campaigns/<id>/images/<image>", methods=['POST'])
def update_campaign_image(id, image):
    return generic_handler(routeKey="POST /brands/me/campaigns/{campaign_id}/images/{image_field}", params={
        "campaign_id": id,
        "image_field": image
    })


@app.route("/campaigns/<id>", methods=['GET'])
def get_campaign_by_id(id):
    return generic_handler(routeKey="GET /campaigns/{campaign_id}", params={"campaign_id": id})


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
