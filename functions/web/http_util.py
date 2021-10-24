import json


class PinfluencerResponse:
    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self.body = body

    def is_ok(self) -> bool:
        return 200 <= self.status_code < 300

    def format(self) -> dict:
        return {
            'statusCode': self.status_code,
            'body': json.dumps(self.body, default=str),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'},
        }
