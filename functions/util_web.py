import json
import uuid

from schema import Schema, Optional, SchemaError

from functions import util_db


class Controller:

    @staticmethod
    def process(event):
        try:
            http_method = Controller.extract_http_method(event)
            resource = event['rawPath'][1:]

            if resource != 'feed':
                resource = resource[:-1]

            # Handle CRUD 
            if http_method == 'post':
                payload_validators['post'][resource].is_valid(event['body'])
                resource_id = util_db.Repository.create(resource, event['body'])
                return HttpUtils.respond(status_code=201,
                                         res=f"Create {resource} successfully. /{resource}s?id={resource_id}")
            elif http_method == 'get':
                formatted = util_db.Repository.get_all(resource)
                return HttpUtils.respond(res=f"Read {resource} Results:\n {formatted}")
            elif http_method == 'put':
                payload_validators['put'][resource].is_valid(event['body'])
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(status_code=400, res=f"Unsupported action {http_method}")

        except SchemaError as validation_error:
            return HttpUtils.respond(error_msg='The payload was invalid', status_code=400)
        except Exception as e:
            Controller.print_exception(e)
            return HttpUtils.respond(error_msg='The server had a problem dealing with this request', status_code=500)

    @staticmethod
    def extract_http_method(event):
        return event['requestContext']['http']['method'].lower()

    @staticmethod
    def print_exception(e):
        print(''.join(['Exception ', str(type(e))]))
        print(''.join(['Exception ', str(e)]))


class HttpUtils:

    @staticmethod
    def respond(error_msg='error', status_code=400, res=None):
        body = error_msg if status_code == 400 else json.dumps(res)
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
    }
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
    }
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
