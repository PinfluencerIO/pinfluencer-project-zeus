import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(event)
    response = Controller.process(event)
    logger.info("response: %s" % response)
    return response


class Controller():
    def __init__(self):
        pass

    @staticmethod
    def process(event):
        try:
            http_method = event['requestContext']['http']['method'].lower()
            resource = event['rawPath'][1:]
            # Handle CRUD 
            if http_method == 'post':
                return HttpUtils.respond(res=f"Create {resource}")
            elif http_method == 'get':
                return HttpUtils.respond(res=f"Read {resource}")
            elif http_method == 'put':
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(err="Unsupported action", err_code=400, res=f"Unsupported action {http_method}")

        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(err=e, err_code=404)

class HttpUtils:
    def __init__(self):
        pass

    @staticmethod
    def respond(err=None, err_code=400, res=None):
        return {
            'statusCode': str(err_code) if err else '200',
            'body': '{"message":%s}' % json.dumps(str(err)) if err else res,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

def print_exception(e):
    logger.error(''.join(['Exception ', str(type(e))]))
    logger.error(''.join(['Exception ', str(e)]))