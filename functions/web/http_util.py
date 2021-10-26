import json


class PinfluencerResponse:
    def __init__(self, status_code: int = 200, body=None):
        if body is None:
            body = {}

        self.status_code = status_code
        self.body = body

    def is_ok(self) -> bool:
        return 200 <= self.status_code < 300

    def as_json(self) -> dict:
        return {
            'statusCode': self.status_code,
            'body': json.dumps(self.body, default=str),
            'headers': {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Methods': '*'},
        }

    @staticmethod
    def as_500_error():
        return PinfluencerResponse(500, {"message": "Unexpected server error. Please try later."})

    @staticmethod
    def as_401_error():
        return PinfluencerResponse(401, {"message": 'Not authorised'})

    @staticmethod
    def as_404_error():
        return PinfluencerResponse(404, {"message": 'Not found'})

    @staticmethod
    def as_400_error():
        return PinfluencerResponse(400, {"message": 'Client error, please check request.'})
