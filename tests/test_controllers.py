import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeCaseDeserializer
from src.domain.models import Brand, ValueEnum, CategoryEnum
from src.domain.validation import BrandValidator
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, InfluencerRepository, AuthUserRepository
from src.web.controllers import BrandController, InfluencerController
from src.web.validation import valid_uuid
from tests import brand_dto_generator, assert_brand_updatable_fields_are_equal, TEST_DEFAULT_BRAND_LOGO, \
    TEST_DEFAULT_BRAND_HEADER_IMAGE, influencer_dto_generator, RepoEnum, user_dto_generator


def get_brand_id_event(brand_id):
    return {'pathParameters': {'brand_id': brand_id}}


def get_auth_user_event(auth_id):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": auth_id}}}}}


def update_brand_payload():
    return {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@gmail.com",
        "brand_name": "name",
        "brand_description": "description",
        "website": "https://website.com",
        "insta_handle": "instahandle",
        "values": ["VALUE7", "VALUE8", "VALUE9"],
        "categories": ["CATEGORY7", "CATEGORY6", "CATEGORY5"]
    }


def update_image_payload():
    return {
        "image_bytes": "random_bytes"
    }


def update_brand_return_dto():
    return Brand(first_name="first_name",
                 last_name="last_name",
                 email="email@gmail.com",
                 brand_name="name",
                 brand_description="description",
                 website="https://website.com",
                 insta_handle="instahandle",
                 values=[ValueEnum.VALUE7, ValueEnum.VALUE8, ValueEnum.VALUE9],
                 categories=[CategoryEnum.CATEGORY7, CategoryEnum.CATEGORY6, CategoryEnum.CATEGORY5])


def create_brand_for_auth_user_event(auth_id, payload):
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": auth_id}}}},
        "body": JsonSnakeToCamelSerializer().serialize(payload)
    }


class TestInfluencerController(TestCase):

    def setUp(self):
        self.__influencer_repository: InfluencerRepository = Mock()
        self.__auth_user_repo: AuthUserRepository = Mock()
        self.__sut = InfluencerController(influencer_repository=self.__influencer_repository,
                                          deserializer=JsonCamelToSnakeCaseDeserializer(),
                                          auth_user_repository=self.__auth_user_repo)

    def test_get_by_id(self):
        influencer = influencer_dto_generator(num=1)
        self.__influencer_repository.load_by_id = MagicMock(return_value=influencer)
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(influencer.id))
        self.__influencer_repository.load_by_id.assert_called_once_with(id_=influencer.id)
        assert pinfluencer_response.body == influencer.__dict__
        assert pinfluencer_response.is_ok() is True

class TestBrandController(TestCase):

    def setUp(self):
        self.__brand_repository: BrandRepository = Mock()
        self.__brand_validator = BrandValidator()
        self.__auth_user_repo: AuthUserRepository = Mock()
        self.__sut = BrandController(brand_repository=self.__brand_repository,
                                     brand_validator=self.__brand_validator,
                                     deserializer=JsonCamelToSnakeCaseDeserializer(),
                                     auth_user_repository=self.__auth_user_repo)

    def test_get_by_id(self):
        brand_from_db = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        user_from_auth_db = user_dto_generator(num=1)
        expected_brand = brand_dto_generator(num=1)
        expected_brand.id = brand_from_db.id
        expected_brand.created = brand_from_db.created
        self.__brand_repository.load_by_id = MagicMock(return_value=brand_from_db)
        self.__auth_user_repo.get_by_id = MagicMock(return_value=user_from_auth_db)
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(brand_from_db.id))
        self.__auth_user_repo.get_by_id.assert_called_once_with(_id=brand_from_db.auth_user_id)
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand_from_db.id)
        assert pinfluencer_response.body == expected_brand.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_get_by_id_when_not_found(self):
        self.__brand_repository.load_by_id = MagicMock(side_effect=NotFoundException())
        field = str(uuid.uuid4())
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(field))
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404

    def test_get_by_id_when_invalid_uuid(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = "12345"
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(field))
        self.__brand_repository.load_by_id.assert_not_called()
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 400

    def test_get_all(self):
        expected_brands = [
            brand_dto_generator(num=1),
            brand_dto_generator(num=2),
            brand_dto_generator(num=3),
            brand_dto_generator(num=4)
        ]
        self.__brand_repository.load_collection = MagicMock(return_value=expected_brands)
        pinfluencer_response = self.__sut.get_all({})
        self.__brand_repository.load_collection.assert_called_once()
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, expected_brands))
        assert pinfluencer_response.status_code == 200

    def test_get(self):
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=expected_brand)
        auth_id = "1234brand1"
        response = self.__sut.get(get_auth_user_event(auth_id))
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == expected_brand.__dict__
        assert response.status_code == 200

    def test_get_when_not_found(self):
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        auth_id = "1234brand1"
        response = self.__sut.get(get_auth_user_event(auth_id))
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == {}
        assert response.status_code == 404

    def test_create(self):
        expected_payload = update_brand_payload()
        auth_id = "1234brand1"
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=update_brand_payload())
        self.__brand_repository.write_new_for_auth_user = MagicMock()
        response = self.__sut.create(event=event)
        payload_captor = Captor()
        self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert actual_payload.logo == TEST_DEFAULT_BRAND_LOGO
        assert actual_payload.header_image == TEST_DEFAULT_BRAND_HEADER_IMAGE
        assert_brand_updatable_fields_are_equal(actual_payload.__dict__, expected_payload)
        assert list(map(lambda x: x.name, actual_payload.values)) == expected_payload['values']
        assert list(map(lambda x: x.name, actual_payload.categories)) == expected_payload['categories']
        assert response.status_code == 201
        assert response.body == actual_payload.__dict__

    def test_create_when_exists(self):
        auth_id = "1234brand1"
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=update_brand_payload())
        self.__brand_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = self.__sut.create(event=event)
        assert response.status_code == 400
        assert response.body == {}

    def test_create_when_invalid_payload(self):
        auth_id = "1234brand1"
        payload = update_brand_payload()
        payload['brand_name'] = 120
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        response = self.__sut.create(event=event)
        assert response.status_code == 400
        assert response.body == {}

    def test_update(self):
        expected_payload = update_brand_payload()
        expected_payload_dto = update_brand_return_dto()
        auth_id = "1234brand1"
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=update_brand_payload())
        self.__brand_repository.update_for_auth_user = MagicMock(return_value=expected_payload_dto)
        response = self.__sut.update(event=event)
        payload_captor = Captor()
        self.__brand_repository.update_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                             payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert_brand_updatable_fields_are_equal(actual_payload.__dict__, expected_payload)
        assert list(map(lambda x: x.name, actual_payload.values)) == expected_payload['values']
        assert list(map(lambda x: x.name, actual_payload.categories)) == expected_payload['categories']
        assert response.status_code == 200
        assert response.body == expected_payload_dto.__dict__

    def test_update_when_invalid_payload(self):
        auth_id = "1234brand1"
        payload = update_brand_payload()
        payload['brand_name'] = 120
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)

        response = self.__sut.update(event=event)
        assert response.status_code == 400
        assert response.body == {}

    def test_update_when_not_found(self):
        auth_id = "1234brand1"
        payload = update_brand_payload()
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        self.__brand_repository.update_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = self.__sut.update(event=event)
        assert response.status_code == 404
        assert response.body == {}

    def test_update_logo(self):
        auth_id = "1234brand1"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        self.__brand_repository.update_logo_for_auth_user = MagicMock(return_value=expected_brand)
        response = self.__sut.update_logo(event=event)
        assert response.status_code == 200
        assert response.body == expected_brand.__dict__

    def test_update_logo_when_not_found(self):
        auth_id = "1234brand1"
        payload = update_image_payload()
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        self.__brand_repository.update_logo_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = self.__sut.update_logo(event=event)
        assert response.status_code == 404
        assert response.body == {}

    def test_update_header_image(self):
        auth_id = "1234brand1"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(return_value=expected_brand)
        response = self.__sut.update_header_image(event=event)
        assert response.status_code == 200
        assert response.body == expected_brand.__dict__

    def test_update_header_image_when_not_found(self):
        auth_id = "1234brand1"
        payload = update_image_payload()
        event = create_brand_for_auth_user_event(auth_id=auth_id, payload=payload)
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = self.__sut.update_header_image(event=event)
        assert response.status_code == 404
        assert response.body == {}
