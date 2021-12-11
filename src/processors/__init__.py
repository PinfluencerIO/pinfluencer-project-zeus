import boto3

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
