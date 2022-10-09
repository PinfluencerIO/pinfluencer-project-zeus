from unittest import TestCase

from src.crosscutting import AutoFixture
from src.domain.models import Brand
from src.web.mapping import MappingRules
from src.web.views import BrandRequestDto, BrandResponseDto
from tests import test_mapper


class TestMappingRules(TestCase):

    def setUp(self) -> None:
        self.__mapper = test_mapper()
        self.__sut = MappingRules(mapper=self.__mapper)
        self.__fixture = AutoFixture()

    def test_map_brand_to_brand_request(self):
        # arrange
        brand = self.__fixture.create(dto=Brand, list_limit=5)

        self.__sut.add_rules()

        # act
        brand_request = self.__mapper.map(_from=brand, to=BrandRequestDto)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand_request.brand_name, brand.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand_request.brand_description, brand.brand_description)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand_request.categories, brand.categories)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(brand_request.values, list(map(lambda x: x.value, brand.values)))

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand_request.website, brand.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand_request.insta_handle, brand.insta_handle)

    def test_map_brand_request_to_brand(self):
        # arrange
        brand_request = self.__fixture.create(dto=BrandRequestDto, list_limit=5)

        self.__sut.add_rules()

        # act
        brand = self.__mapper.map(_from=brand_request, to=Brand)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand.brand_name, brand_request.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand.brand_description, brand_request.brand_description)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand.categories, brand_request.categories)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(list(map(lambda x: x.value, brand.values)), brand_request.values)

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand.website, brand_request.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand.insta_handle, brand_request.insta_handle)

    def test_map_brand_to_brand_response(self):
        # arrange
        brand = self.__fixture.create(dto=Brand, list_limit=5)

        self.__sut.add_rules()

        # act
        brand_response = self.__mapper.map(_from=brand, to=BrandResponseDto)

        # assert
        with self.subTest(msg="brand id matches"):
            self.assertEqual(brand_response.id, brand.id)

        # assert
        with self.subTest(msg="brand created date matches"):
            self.assertEqual(brand_response.created, brand.created)

        # assert
        with self.subTest(msg="brand auth user id matches"):
            self.assertEqual(brand_response.auth_user_id, brand.auth_user_id)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand_response.brand_name, brand.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand_response.brand_description, brand.brand_description)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand_response.categories, brand.categories)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(brand_response.values, list(map(lambda x: x.value, brand.values)))

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand_response.website, brand.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand_response.insta_handle, brand.insta_handle)

    def test_map_brand_response_to_brand(self):
        # arrange
        brand_response = self.__fixture.create(dto=BrandResponseDto, list_limit=5)

        self.__sut.add_rules()

        # act
        brand = self.__mapper.map(_from=brand_response, to=Brand)

        # assert
        with self.subTest(msg="brand id matches"):
            self.assertEqual(brand_response.id, brand.id)

        # assert
        with self.subTest(msg="brand created date matches"):
            self.assertEqual(brand_response.created, brand.created)

        # assert
        with self.subTest(msg="brand auth user id matches"):
            self.assertEqual(brand_response.auth_user_id, brand.auth_user_id)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand.brand_name, brand_response.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand.brand_description, brand_response.brand_description)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand.categories, brand_response.categories)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(list(map(lambda x: x.value, brand.values)), brand_response.values)

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand.website, brand_response.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand.insta_handle, brand_response.insta_handle)
