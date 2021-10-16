from .util_log import print_exception
from .util_http import HttpUtils
from .util_db import *

class Controller():
    def __init__(self):
        pass

    @staticmethod
    def process(event):
        try:
            http_method = Controller.extract_http_method(event)
            resource = event['rawPath'][1:-1]
            # Handle CRUD 
            if http_method == 'post':
                return HttpUtils.respond(res=f"Create {resource}")
            elif http_method == 'get':
                formatted = formatRecords(executeQuery(f'SELECT * FROM {resource}')['records'])
                return HttpUtils.respond(res=f"Read {resource} Results:\n {formatted}")
            elif http_method == 'put':
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(err="Unsupported action", err_code=400, res=f"Unsupported action {http_method}")

        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(err=e, err_code=404)

    @staticmethod
    def extract_http_method(event):
        return event['requestContext']['http']['method'].lower()
