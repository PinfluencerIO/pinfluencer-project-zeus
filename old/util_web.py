import json

from schema import Schema, Optional, SchemaError

from functions import util_db
from functions.http_util import HttpUtils
from functions.log_util import print_exception


# todo handle images brand.logo and product.image
class Controller:

    @classmethod
    def process(cls, action, resource, authorizer, payload):
        try:
            if action in methods:
                return methods[action](action, resource, authorizer, payload)
            else:
                return HttpUtils.respond(status_code=400, res=f"Unsupported action {action}")

        except SchemaError as validation_error:
            print_exception(validation_error)
            return HttpUtils.respond(error_msg='The payload was invalid', status_code=400)
        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(error_msg='The server had a problem dealing with this request', status_code=500)

    @classmethod
    def do_process(cls, action, resource, authorizer, payload):
        pass


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


def _do_post(event, resource):
    payload_ = json.loads(event['body'])
    payload_validators['post'][resource].is_valid(payload_)
    # todo handle no email
    payload_['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
    payload_['auth_user'] = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    resource_id = util_db.Repository.create(resource, payload_)
    return HttpUtils.respond(status_code=201,
                             res=f"Create {resource} successfully. /{resource}s?id={resource_id}")


def _do_get(event, resource):
    print(f"! {resource}")
    if 'queryStringParameters' in event:
        print(f"!! has query")
        if 'id' in event['queryStringParameters'] and valid_uuid(event['queryStringParameters']['id']):
            print(f"!!! has id and is valid")
            formatted_as_json = util_db.Repository.get_by_id(resource,
                                                             event['queryStringParameters']['id'])
            print(f"!!!! {formatted_as_json}")
        else:
            return HttpUtils.respond('bad query')
    else:
        formatted_as_json = util_db.Repository.get_all(resource)

    return HttpUtils.respond(status_code=200, res=formatted_as_json)


def _do_put(event, resource):
    payload_ = json.loads(event['body'])
    payload_validators['put'][resource].is_valid(payload_)
    return HttpUtils.respond(res=f"Update {resource}")


def _do_delete(event, resource):
    return HttpUtils.respond(res=f"Delete {resource}")


methods = {
    'post': _do_post,
    'get': _do_get,
    'put': _do_put,
    'delete': _do_delete
}
