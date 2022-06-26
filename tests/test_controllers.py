import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src.crosscutting import JsonCamelToSnakeCaseDeserializer
from src.domain.models import Influencer
from src.domain.validation import BrandValidator, InfluencerValidator
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, InfluencerRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController
from src.web.validation import valid_uuid
from tests import brand_dto_generator, assert_brand_updatable_fields_are_equal, TEST_DEFAULT_BRAND_LOGO, \
    TEST_DEFAULT_BRAND_HEADER_IMAGE, influencer_dto_generator, RepoEnum, \
    assert_brand_creatable_generated_fields_are_equal, TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE, \
    assert_influencer_creatable_generated_fields_are_equal, assert_influencer_update_fields_are_equal, \
    get_influencer_id_event, get_brand_id_event, update_brand_payload, create_brand_dto, \
    update_image_payload, update_brand_return_dto, create_influencer_dto, \
    update_influencer_payload


class TestInfluencerController(TestCase):

    def setUp(self):
        self.__influencer_repository: InfluencerRepository = Mock()
        self.__sut = InfluencerController(influencer_repository=self.__influencer_repository,
                                          deserializer=JsonCamelToSnakeCaseDeserializer(),
                                          influencer_validator=InfluencerValidator())

    def test_get_by_id(self):
        # arrange
        influencer_in_db = influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__influencer_repository.load_by_id = MagicMock(return_value=influencer_in_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(response=pinfluencer_response,
                                                event=get_influencer_id_event(influencer_in_db.id)))

        # assert
        assert pinfluencer_response.body == influencer_in_db.__dict__

    def test_get(self):
        # arrange
        db_influencer = influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__influencer_repository.load_for_auth_user = MagicMock(return_value=db_influencer)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(response=response,
                                          auth_user_id=auth_id))

        # assert
        assert response.body == db_influencer.__dict__
        assert response.status_code == 200

    def test_get_all(self):
        # arrange
        influencers_from_db = [
            influencer_dto_generator(num=1, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=2, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=3, repo=RepoEnum.STD_REPO),
            influencer_dto_generator(num=4, repo=RepoEnum.STD_REPO)
        ]
        self.__influencer_repository.load_collection = MagicMock(return_value=influencers_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(response=pinfluencer_response,
                                              event={}))

        # assert
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, influencers_from_db))
        assert pinfluencer_response.status_code == 200

    def test_create(self):
        # arrange
        influencer_db = create_influencer_dto()
        expected_payload = update_influencer_payload()
        auth_id = "1234"
        self.__influencer_repository.write_new_for_auth_user = MagicMock(return_value=influencer_db)
        response = PinfluencerResponse()

        # act
        self.__sut.create(PinfluencerContext(response=response,
                                             body=expected_payload,
                                             auth_user_id=auth_id))

        # assert
        payload_captor = Captor()
        self.__influencer_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                     payload=payload_captor)
        actual_payload: Influencer = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert actual_payload.image == TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE
        assert_influencer_creatable_generated_fields_are_equal(expected_payload, actual_payload.__dict__)
        assert response.status_code == 201
        assert response.body == actual_payload.__dict__
        print(response.body)

    def test_create_when_exists(self):
        # arrange
        auth_id = "12341"
        payload = update_influencer_payload()
        self.__influencer_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_create_when_invalid_payload(self):
        # arrange
        auth_id = "12341"
        payload = update_influencer_payload()
        payload['bio'] = 120
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_profile_image(self):

        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_influencer = influencer_dto_generator(num=1)
        self.__influencer_repository.update_image_for_auth_user = MagicMock(return_value=expected_influencer)
        response = PinfluencerResponse()

        # act
        self.__sut.update_profile_image(PinfluencerContext(body=payload,
                                                           auth_user_id=auth_id,
                                                           response=response))

        # assert
        assert response.status_code == 200
        assert response.body == expected_influencer.__dict__

    def test_update(self):
        # arrange
        influencer_in_db = create_influencer_dto()
        self.__influencer_repository.update_for_auth_user = MagicMock(return_value=influencer_in_db)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.update(PinfluencerContext(
            auth_user_id=auth_id, body=update_influencer_payload(),
            response=response))

        # assert
        arg_captor = Captor()
        self.__influencer_repository.update_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                  payload=arg_captor)
        update_for_auth_user_repo_payload: Influencer = arg_captor.arg
        assert_influencer_update_fields_are_equal(influencer1=update_influencer_payload(),
                                                  influencer2=update_for_auth_user_repo_payload.__dict__)
        assert list(map(lambda x: x.name, update_for_auth_user_repo_payload.values)) == update_influencer_payload()[
            "values"]
        assert list(map(lambda x: x.name, update_for_auth_user_repo_payload.categories)) == update_influencer_payload()[
            "categories"]
        assert response.body == influencer_in_db.__dict__
        assert response.status_code == 200

    def test_update_when_not_found(self):
        # arrange
        self.__influencer_repository.update_for_auth_user = MagicMock(
            side_effect=NotFoundException("influencer not found"))
        return_value = PinfluencerResponse()

        # act
        context = PinfluencerContext(
            auth_user_id="12341", body=update_influencer_payload(),
            response=return_value)
        self.__sut.update(context)

        # assert
        assert return_value.body == {}
        assert return_value.status_code == 404
        assert context.short_circuit == True

    def test_update_when_payload_not_valid(self):
        # arrange
        payload = update_influencer_payload()
        payload['bio'] = 120
        return_value = PinfluencerResponse()

        # act
        context = PinfluencerContext(auth_user_id="12341", body=payload,
                                     response=return_value)
        self.__sut.update(context)

        # assert
        assert return_value.body == {}
        assert return_value.status_code == 400
        assert context.short_circuit == True


class TestBrandController(TestCase):

    def setUp(self):
        self.__brand_repository: BrandRepository = Mock()
        self.__brand_validator = BrandValidator()
        self.__sut = BrandController(brand_repository=self.__brand_repository,
                                     brand_validator=self.__brand_validator,
                                     deserializer=JsonCamelToSnakeCaseDeserializer())

    def test_get_by_id(self):
        # arrange
        brand_from_db = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_by_id(PinfluencerContext(event=get_brand_id_event(brand_from_db.id),
                                                response=pinfluencer_response))

        # assert
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand_from_db.id)
        assert pinfluencer_response.body == brand_from_db.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_get_by_id_when_not_found(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock(side_effect=NotFoundException())
        field = str(uuid.uuid4())
        pinfluencer_response = PinfluencerResponse()

        # act
        context = PinfluencerContext(event=get_brand_id_event(field), response=pinfluencer_response)
        self.__sut.get_by_id(context)

        # assert
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404
        assert context.short_circuit == True

    def test_get_by_id_when_invalid_uuid(self):
        # arrange
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = "12345"
        pinfluencer_response = PinfluencerResponse()

        # act
        context = PinfluencerContext(event=get_brand_id_event(field), response=pinfluencer_response)
        self.__sut.get_by_id(context)

        # assert
        self.__brand_repository.load_by_id.assert_not_called()
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 400
        assert context.short_circuit == True

    def test_get_all(self):
        # arrange
        brands_from_db = [
            brand_dto_generator(num=1, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=2, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=3, repo=RepoEnum.STD_REPO),
            brand_dto_generator(num=4, repo=RepoEnum.STD_REPO)
        ]
        self.__brand_repository.load_collection = MagicMock(return_value=brands_from_db)
        pinfluencer_response = PinfluencerResponse()

        # act
        self.__sut.get_all(PinfluencerContext(event={},
                                              response=pinfluencer_response))

        # assert
        self.__brand_repository.load_collection.assert_called_once()
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, brands_from_db))
        assert pinfluencer_response.status_code == 200

    def test_get(self):
        # arrange
        db_brand = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=db_brand)
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        self.__sut.get(PinfluencerContext(auth_user_id=auth_id,
                                          response=response))

        # assert
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == db_brand.__dict__
        assert response.status_code == 200

    def test_get_when_not_found(self):
        # arrange
        self.__brand_repository.load_for_auth_user = MagicMock(side_effect=NotFoundException())
        auth_id = "12341"
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(auth_user_id=auth_id, response=response)
        self.__sut.get(context)

        # assert
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == {}
        assert response.status_code == 404
        assert context.short_circuit == True

    def test_create(self):
        # arrange
        brand_db = create_brand_dto()
        expected_payload = update_brand_payload()
        auth_id = "12341"
        self.__brand_repository.write_new_for_auth_user = MagicMock(return_value=brand_db)
        response = PinfluencerResponse()

        # act
        self.__sut.create(PinfluencerContext(body=expected_payload,
                                             auth_user_id=auth_id,
                                             response=response))

        # assert
        payload_captor = Captor()
        self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                                payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert actual_payload.logo == TEST_DEFAULT_BRAND_LOGO
        assert actual_payload.header_image == TEST_DEFAULT_BRAND_HEADER_IMAGE
        assert_brand_creatable_generated_fields_are_equal(expected_payload, actual_payload.__dict__)
        assert response.status_code == 201
        assert response.body == actual_payload.__dict__
        print(response.body)

    def test_create_when_exists(self):

        # arrange
        auth_id = "12341"
        self.__brand_repository.write_new_for_auth_user = MagicMock(side_effect=AlreadyExistsException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(auth_user_id=auth_id, response=response)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_create_when_invalid_payload(self):
        # arrange
        auth_id = "12341"
        payload = update_brand_payload()
        payload['brand_name'] = 120
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.create(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_update(self):
        # arrange
        expected_payload = update_brand_payload()
        brand_in_db = update_brand_return_dto()
        auth_id = "12341"
        self.__brand_repository.update_for_auth_user = MagicMock(return_value=brand_in_db)
        response = PinfluencerResponse()

        # act
        self.__sut.update(PinfluencerContext(body=expected_payload,
                                             auth_user_id=auth_id,
                                             response=response))

        # assert
        payload_captor = Captor()
        self.__brand_repository.update_for_auth_user.assert_called_once_with(auth_user_id=auth_id,
                                                                             payload=payload_captor)
        actual_payload = payload_captor.arg
        assert valid_uuid(actual_payload.id)
        assert_brand_updatable_fields_are_equal(actual_payload.__dict__, expected_payload)
        assert list(map(lambda x: x.name, actual_payload.values)) == expected_payload['values']
        assert list(map(lambda x: x.name, actual_payload.categories)) == expected_payload['categories']
        assert response.status_code == 200
        assert response.body == brand_in_db.__dict__

    def test_update_when_invalid_payload(self):
        # arrange
        auth_id = "12341"
        payload = update_brand_payload()
        payload['brand_name'] = 120
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(auth_user_id=auth_id, body=payload, response=response)
        self.__sut.update(context)

        # assert
        assert response.status_code == 400
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_brand_payload()
        self.__brand_repository.update_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_logo(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.update_logo_for_auth_user = MagicMock(return_value=expected_brand)
        response = PinfluencerResponse()

        # act
        self.__sut.update_logo(PinfluencerContext(auth_user_id=auth_id,
                                                  body=payload,
                                                  response=response))

        # assert
        assert response.status_code == 200
        assert response.body == expected_brand.__dict__

    def test_update_logo_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        self.__brand_repository.update_logo_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update_logo(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True

    def test_update_header_image(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(return_value=expected_brand)
        response = PinfluencerResponse()

        # act
        self.__sut.update_header_image(PinfluencerContext(body=payload,
                                                          auth_user_id=auth_id,
                                                          response=response))

        # assert
        assert response.status_code == 200
        assert response.body == expected_brand.__dict__

    def test_update_header_image_when_not_found(self):
        # arrange
        auth_id = "12341"
        payload = update_image_payload()
        self.__brand_repository.update_header_image_for_auth_user = MagicMock(side_effect=NotFoundException())
        response = PinfluencerResponse()

        # act
        context = PinfluencerContext(body=payload, auth_user_id=auth_id, response=response)
        self.__sut.update_header_image(context)

        # assert
        assert response.status_code == 404
        assert response.body == {}
        assert context.short_circuit == True
