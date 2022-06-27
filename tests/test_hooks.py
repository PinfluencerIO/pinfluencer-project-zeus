from unittest import TestCase
from unittest.mock import Mock, MagicMock, call
from uuid import uuid4

from callee import Captor

from src.crosscutting import JsonCamelToSnakeCaseDeserializer
from src.domain.models import User, Brand, Influencer
from src.domain.validation import InfluencerValidator, BrandValidator
from src.types import AuthUserRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.hooks import UserAfterHooks, UserBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, CommonBeforeHooks, \
    InfluencerBeforeHooks, BrandBeforeHooks
from tests import brand_dto_generator, RepoEnum, get_auth_user_event, create_for_auth_user_event, get_brand_id_event, \
    get_influencer_id_event


class TestBrandBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__brand_validator = BrandValidator()
        self.__sut = BrandBeforeHooks(brand_validator=self.__brand_validator)

    def test_validate_uuid(self):
        # arrange
        context = PinfluencerContext(event=get_brand_id_event(brand_id=str(uuid4())),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_uuid_when_invalid(self):
        # arrange
        context = PinfluencerContext(event=get_brand_id_event(brand_id="boo"),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert context.short_circuit
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_validate_brand_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "brand_name": "my brand",
            "brand_description": "this is my brand",
            "website": "https://brand.com"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_brand_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "brand_name": "my brand",
            "brand_description": "this is my brand",
            "website": "invalid website"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_brand(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}


class TestInfluencerBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__influencer_validator = InfluencerValidator()
        self.__sut = InfluencerBeforeHooks(influencer_validator=self.__influencer_validator)

    def test_validate_uuid(self):

        # arrange
        context = PinfluencerContext(event=get_influencer_id_event(id=str(uuid4())),
                                     short_circuit=False)

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_uuid_when_invalid(self):
        # arrange
        context = PinfluencerContext(event=get_influencer_id_event(id="boo"),
                                     short_circuit=False,
                                     response=PinfluencerResponse())

        # act
        self.__sut.validate_uuid(context=context)

        # assert
        assert context.short_circuit
        assert context.response.status_code == 400
        assert context.response.body == {}

    def test_validate_influencer_when_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "bio": "my brand",
            "website": "https://brand.com"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_influencer(context=context)

        # assert
        assert not context.short_circuit

    def test_validate_influencer_when_not_valid(self):
        # arrange
        context = PinfluencerContext(body={
            "bio": "this is my brand",
            "website": "invalid website"
        }, response=PinfluencerResponse(), short_circuit=False)

        # act
        self.__sut.validate_influencer(context=context)

        # assert
        assert context.short_circuit == True
        assert context.response.status_code == 400
        assert context.response.body == {}


class TestCommonHooks(TestCase):

    def setUp(self) -> None:
        self.__deserializer = JsonCamelToSnakeCaseDeserializer()
        self.__sut = CommonBeforeHooks(deserializer=self.__deserializer)

    def test_set_body(self):
        # arrange
        body = {
            "first_name": "aidan",
            "last_name": "aidan",
            "email": "aidanwilliamgannon@gmail.com"
        }
        pinfluencer_context = PinfluencerContext(event=create_for_auth_user_event(auth_id="1234",
                                                                                  payload=body))

        # act
        self.__sut.set_body(context=pinfluencer_context)

        # assert
        assert pinfluencer_context.body == body


class TestBrandAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__sut = BrandAfterHooks(auth_user_repository=self.__auth_user_repository)

    def test_set_brand_claims(self):
        # arrange
        self.__auth_user_repository.update_brand_claims = MagicMock()
        auth_user_id = "12341"
        first_name = "aidan"
        last_name = "gannon"
        email = "aidanwilliamgannon@gmail.com"
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body={
                                         "first_name": first_name,
                                         "last_name": last_name,
                                         "email": email
                                     })

        # act
        self.__sut.set_brand_claims(context=context)

        # assert
        captor = Captor()
        self.__auth_user_repository.update_brand_claims.assert_called_once_with(user=captor)
        user_payload_arg: Brand = captor.arg
        assert user_payload_arg.first_name == first_name
        assert user_payload_arg.last_name == last_name
        assert user_payload_arg.email == email
        assert user_payload_arg.auth_user_id == auth_user_id


class TestInfluencerAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__sut = InfluencerAfterHooks(auth_user_repository=self.__auth_user_repository)

    def test_set_brand_claims(self):
        # arrange
        self.__auth_user_repository.update_influencer_claims = MagicMock()
        auth_user_id = "12341"
        first_name = "aidan"
        last_name = "gannon"
        email = "aidanwilliamgannon@gmail.com"
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     auth_user_id=auth_user_id,
                                     body={
                                         "first_name": first_name,
                                         "last_name": last_name,
                                         "email": email
                                     })

        # act
        self.__sut.set_influencer_claims(context=context)

        # assert
        captor = Captor()
        self.__auth_user_repository.update_influencer_claims.assert_called_once_with(user=captor)
        user_payload_arg: Influencer = captor.arg
        assert user_payload_arg.first_name == first_name
        assert user_payload_arg.last_name == last_name
        assert user_payload_arg.email == email
        assert user_payload_arg.auth_user_id == auth_user_id


class TestUserBeforeHooks(TestCase):

    def setUp(self) -> None:
        self.__sut = UserBeforeHooks()

    def test_set_auth_user_id(self):
        # arrange
        response = PinfluencerResponse()
        auth_id = "12341"

        # act
        context = PinfluencerContext(response=response, event=get_auth_user_event(auth_id=auth_id))
        self.__sut.set_auth_user_id(context=context)

        # assert
        assert context.auth_user_id == auth_id


class TestUserAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__sut = UserAfterHooks(auth_user_repository=self.__auth_user_repository)

    def test_tag_auth_user_claims_to_response(self):
        # arrange
        brand = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        response = PinfluencerResponse(body=brand.__dict__)
        auth_user = User(first_name="cognito_first_name",
                         last_name="cognito_last_name",
                         email="cognito_email")
        self.__auth_user_repository.get_by_id = MagicMock(return_value=auth_user)

        # act
        self.__sut.tag_auth_user_claims_to_response(context=PinfluencerContext(response=response,
                                                                               event={}))

        # assert
        assert response.body["first_name"] == auth_user.first_name
        assert response.body["last_name"] == auth_user.last_name
        assert response.body["email"] == auth_user.email
        self.__auth_user_repository.get_by_id.assert_called_once_with(_id=brand.auth_user_id)

    def test_tag_auth_user_claims_to_response_collection(self):
        # arrange
        users = [
            User(first_name="cognito_first_name1",
                 last_name="cognito_last_name1",
                 email="cognito_email1"),
            User(first_name="cognito_first_name2",
                 last_name="cognito_last_name2",
                 email="cognito_email2"),
            User(first_name="cognito_first_name3",
                 last_name="cognito_last_name3",
                 email="cognito_email3")
        ]
        brands = [
            brand_dto_generator(num=1).__dict__,
            brand_dto_generator(num=2).__dict__,
            brand_dto_generator(num=3).__dict__
        ]
        self.__auth_user_repository.get_by_id = MagicMock(side_effect=users)
        response = PinfluencerResponse(body=brands)

        # act
        self.__sut.tag_auth_user_claims_to_response_collection(context=PinfluencerContext(response=response,
                                                                                          event={}))

        # assert
        assert response.body[0]["first_name"] == users[0].first_name
        assert response.body[0]["last_name"] == users[0].last_name
        assert response.body[0]["email"] == users[0].email

        assert response.body[1]["first_name"] == users[1].first_name
        assert response.body[1]["last_name"] == users[1].last_name
        assert response.body[1]["email"] == users[1].email

        assert response.body[2]["first_name"] == users[2].first_name
        assert response.body[2]["last_name"] == users[2].last_name
        assert response.body[2]["email"] == users[2].email

        self.__auth_user_repository.get_by_id.assert_has_calls(calls=[
            call(_id=brands[0]["auth_user_id"]),
            call(_id=brands[1]["auth_user_id"]),
            call(_id=brands[2]["auth_user_id"])
        ])
