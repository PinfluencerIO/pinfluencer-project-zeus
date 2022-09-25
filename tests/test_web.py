from unittest import TestCase

from ddt import ddt, data

from src.crosscutting import JsonSnakeToCamelSerializer
from src.web import PinfluencerResponse

@ddt
class TestPinfluencerResponse(TestCase):

    @data(200,
          204,
          201,
          299)
    def test_is_ok_when_response_is_200(self, status):
        # assert
        assert PinfluencerResponse(status_code=status).is_ok() == True

    @data(100,
          199,
          400,
          300,
          301,
          401,
          500,
          404)
    def test_is_ok_when_response_is_not_200(self, status):
        assert PinfluencerResponse(status_code=status).is_ok() == False

    def test_to_json(self):
        # arrange
        pinf_response = PinfluencerResponse(body={
            "first_name": "Aidan",
            "last_name": "Gannon",
            "years_old": 22
        })
        expected_json = {"statusCode": 200, "body": """{"firstName": "Aidan", "lastName": "Gannon", "yearsOld": 22}""",
                         "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*",
                                     "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "*"}}

        # act/assert
        assert pinf_response.as_json(serializer=JsonSnakeToCamelSerializer()) == expected_json
