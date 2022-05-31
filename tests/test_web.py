from unittest import TestCase

from src.crosscutting import JsonSnakeToCamelSerializer
from src.web import PinfluencerResponse


class TestPinfluencerResponse(TestCase):

    def test_is_ok_when_response_is_200(self):
        assert PinfluencerResponse().is_ok() == True
        assert PinfluencerResponse(status_code=204).is_ok() == True
        assert PinfluencerResponse(status_code=201).is_ok() == True
        assert PinfluencerResponse(status_code=299).is_ok() == True

    def test_is_ok_when_response_is_not_200(self):
        assert PinfluencerResponse(status_code=100).is_ok() == False
        assert PinfluencerResponse(status_code=199).is_ok() == False
        assert PinfluencerResponse(status_code=400).is_ok() == False
        assert PinfluencerResponse(status_code=300).is_ok() == False
        assert PinfluencerResponse(status_code=301).is_ok() == False
        assert PinfluencerResponse(status_code=401).is_ok() == False
        assert PinfluencerResponse(status_code=500).is_ok() == False
        assert PinfluencerResponse(status_code=404).is_ok() == False

    def test_to_json(self):
        pinf_response = PinfluencerResponse(body={
            "first_name": "Aidan",
            "last_name": "Gannon",
            "years_old": 22
        })

        expected_json = {"statusCode": 200, "body": """{"firstName": "Aidan", "lastName": "Gannon", "yearsOld": 22}""", "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "*"}}

        assert pinf_response.as_json(serializer=JsonSnakeToCamelSerializer()) == expected_json
