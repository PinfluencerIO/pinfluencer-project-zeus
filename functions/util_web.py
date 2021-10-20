import json
import uuid

from schema import Schema, Optional, SchemaError

from functions import util_db


class Controller:

    @staticmethod
    def process(event):
        print(event)
        try:
            http_method = Controller._extract_http_method(event)
            resource = event['rawPath'][1:]

            if resource != 'feed':
                resource = resource[:-1]

            # Handle CRUD
            # todo create dict of methods with common interface, and simplify this block
            if http_method == 'post':
                return Controller.do_post(event, resource)
            elif http_method == 'get':
                if 'queryStringParameters' in event:
                    if 'id' in event['queryStringParameters'] and valid_uuid(id):
                        formatted_as_json = util_db.Repository.get_by_id(resource,
                                                                         event['queryStringParameters']['id'])
                    else:
                        return HttpUtils.respond('bad query')
                else:
                    formatted_as_json = util_db.Repository.get_all(resource)

                return HttpUtils.respond(status_code=200, res=formatted_as_json)
            elif http_method == 'put':
                payload_ = json.loads(event['body'])
                payload_validators['put'][resource].is_valid(payload_)
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(status_code=400, res=f"Unsupported action {http_method}")

        except SchemaError as validation_error:
            Controller.print_exception(validation_error)
            return HttpUtils.respond(error_msg='The payload was invalid', status_code=400)
        except Exception as e:
            Controller.print_exception(e)
            return HttpUtils.respond(error_msg='The server had a problem dealing with this request', status_code=500)

    # todo handle images brand.logo and product.image
    @staticmethod
    def do_post(event, resource):
        payload_ = json.loads(event['body'])
        payload_validators['post'][resource].is_valid(payload_)
        # todo handle no email
        payload_['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
        payload_['auth_user'] = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
        resource_id = util_db.Repository.create(resource, payload_)
        return HttpUtils.respond(status_code=201,
                                 res=f"Create {resource} successfully. /{resource}s?id={resource_id}")

    @staticmethod
    def _extract_http_method(event):
        return event['requestContext']['http']['method'].lower()

    @staticmethod
    def print_exception(e):
        print(''.join(['Exception ', str(type(e))]))
        print(''.join(['Exception ', str(e)]))


class HttpUtils:

    @staticmethod
    def respond(error_msg='error', status_code=400, res=None):
        body = error_msg if status_code == 400 else res
        return {
            'statusCode': status_code,
            'body': body,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }


brand_create_schema = Schema({
    'name': str,
    'description': str,
    'website': str,
    'email': str,
    Optional('logo'): {
        'name': str,
        'bytes': str
    }
})

brand_update_schema = Schema({
    'id': str,
    'name': str,
    'description': str,
    'website': str,
    'email': str,
    Optional('logo'): {
        'name': str,
        'bytes': str
    },
    'version': int
})

product_create_schema = Schema({
    'name': str,
    'description': str,
    Optional('image'): {
        'name': str,
        'bytes': str
    },
    'requirements': str
})

product_update_schema = Schema({
    'id': str,
    'name': str,
    'description': str,
    Optional('image'): {
        'name': str,
        'bytes': str
    },
    'requirements': str,
    'brand': {
        "id": str,
        "name": str
    },
    'version': int
})

payload_validators = {
    'post': {
        'brand': brand_create_schema,
        'product': product_create_schema
    },
    'put': {
        'brand': brand_update_schema,
        'product': product_update_schema
    }
}


def valid_uuid(id_):
    try:
        val = uuid.UUID(id_, version=4)

        # If the uuid_string is a valid hex code,
        # but an invalid uuid4,
        # the UUID.__init__ will convert it to a
        # valid uuid4. This is bad for validation purposes.
        # Therefore, try and match str with UUID
        if str(val) == id_:
            return True
        else:
            return False
    except ValueError:
        return False
