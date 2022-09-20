from unittest import TestCase

from src.crosscutting import JsonSnakeToCamelSerializer, AutoFixture
from src.domain.models import Brand
from src.web import PinfluencerResponse, RequestDtoMapper
from src.web.views import BrandRequestDto


class TestRequestDtoMapper(TestCase):

    def setUp(self) -> None:
        self.__sut = RequestDtoMapper()

    def test_map(self):
        # arrange
        brand_request: BrandRequestDto = AutoFixture().create(dto=BrandRequestDto, list_limit=5)

        # act
        brand: Brand = self.__sut.map(_from=brand_request, to=Brand)

        # assert
        assert brand.brand_name == brand_request.brand_name
        assert brand.brand_description == brand_request.brand_description
        assert brand.values == brand_request.values
        assert brand.logo == brand_request.logo
        assert brand.categories == brand_request.categories
        assert brand.insta_handle == brand_request.insta_handle
        assert brand.website == brand_request.website
        assert brand.header_image == brand_request.header_image





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

        # arrange
        pinf_response = PinfluencerResponse(body={
            "first_name": "Aidan",
            "last_name": "Gannon",
            "years_old": 22
        })
        expected_json = {"statusCode": 200, "body": """{"firstName": "Aidan", "lastName": "Gannon", "yearsOld": 22}""", "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "*"}}

        # act/assert
        assert pinf_response.as_json(serializer=JsonSnakeToCamelSerializer()) == expected_json
