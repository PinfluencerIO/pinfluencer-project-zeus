import uuid

from src.crosscutting import print_exception


def valid_uuid(id_):
    try:
        val = uuid.UUID(id_, version=4)
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            print_exception(f'equality failed {val} {id_}')
    except ValueError as ve:
        print_exception(ve)
    except AttributeError as e:
        print_exception(e)

    return False


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


def protect_email_from_update_if_held_in_claims(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        print(f"Found email in claim: {event['requestContext']['authorizer']['jwt']['claims']['email']}")
        print(f'before {body}')
        body['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
        print(f'after {body}')


