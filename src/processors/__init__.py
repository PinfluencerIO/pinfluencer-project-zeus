import boto3

from src.filters.valid_id_filters import valid_uuid

BUCKET = 'pinfluencer-product-images'

s3 = boto3.client('s3')


def get_user(event):
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
