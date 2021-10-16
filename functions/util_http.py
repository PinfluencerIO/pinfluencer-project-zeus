import json

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