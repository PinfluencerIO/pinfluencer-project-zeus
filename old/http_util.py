import json


class HttpUtils:

    @staticmethod
    def respond(error_msg='error', status_code=400, res=None):
        body = error_msg if status_code == 400 else res
        return {
            'statusCode': status_code,
            'body': body,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }


class PinfluencerResponse:
    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self.body = body

    def is_ok(self) -> bool:
        return 200 <= self.status_code < 300

    def format(self) -> dict:
        return {
            'statusCode': self.status_code,
            'body': json.dumps(self.body),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }
