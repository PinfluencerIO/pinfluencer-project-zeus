import json
import uuid

from schema import Schema, Optional

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
                payload_validators[resource].is_valid(event['body'])
                resource_id = util_db.Repository.create(resource, event['body'])
                return HttpUtils.respond(status_code=201,
                                         res=f"Create {resource} successfully. /{resource}s?id={resource_id}")
            elif http_method == 'get':
                formatted = util_db.Repository.get_all(resource)
                return HttpUtils.respond(res=f"Read {resource} Results:\n {formatted}")
            elif http_method == 'put':
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(err="Unsupported action", status_code=400, res=f"Unsupported action {http_method}")

        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(err=e, status_code=404)

    @staticmethod
    def extract_http_method(event):
        return event['requestContext']['http']['method'].lower()


class HttpUtils:

    @staticmethod
    def respond(err=None, status_code=400, res=None):
        print(err)
        body = 'error' if status_code == 400 else json.dumps(res)
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

product_create_schema = Schema({
    'name': str,
    'description': str,
    Optional('image'): {
        'name': str,
        'bytes': str
    },
    'requirements': str
})

payload_validators = {
    'brand': brand_create_schema,
    'product': product_create_schema
}


def print_exception(e):
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))
