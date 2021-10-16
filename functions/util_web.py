try:
    import util_db
except:
    import functions.util_db
    
import json

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
                formatted = util_db.Respository.get_all(resource)
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
    print(''.join(['Exception ', str(type(e))]))
    print(''.join(['Exception ', str(e)]))