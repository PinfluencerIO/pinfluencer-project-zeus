import json
from dataclasses import dataclass

from flask import Flask, request, Response

from src.app import lambda_handler
from src.crosscutting import PinfluencerObjectMapper

app = Flask(__name__)


@dataclass(unsafe_hash=True)
class PinfResponse:
    body: str = None
    headers: dict = None

    # Violates naming but this is only for local testing so dw about it
    statusCode: int = None


@app.route("/<auth_user>/brands/me/images/<image>", methods=['POST'])
def update_brand_logo(auth_user, image):
    return generic_handler(routeKey="POST /brands/me/images/{image_field}",
                           params={
                               "image_field": image
                           },
                           auth_user=auth_user)


@app.route("/<auth_user>/brands/me", methods=['GET'])
def get_brand_for_auth_user(auth_user):
    return generic_handler(routeKey="GET /brands/me", params={}, auth_user=auth_user)


@app.route("/<auth_user>/brands/me", methods=['POST'])
def create_brand_for_auth_user(auth_user):
    return generic_handler(routeKey="POST /brands/me", params={}, auth_user=auth_user)


def generic_handler(routeKey: str, params: dict, auth_user: str):
    body_string = None
    try:
        body = request.json
        body_string = json.dumps(body)
    except Exception:
        ...
    if body_string is None:
        body_string = ""
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
    response_object: PinfResponse = PinfluencerObjectMapper().map_from_dict(_from=response, to=PinfResponse)
    return Response(response_object.body,
                    status=response_object.statusCode,
                    mimetype='application/json')
