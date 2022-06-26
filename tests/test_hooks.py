from unittest import TestCase
from unittest.mock import Mock, MagicMock, call

from callee import Captor

from src.domain.models import User
from src.types import AuthUserRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.hooks import UserAfterHooks, UserBeforeHooks, BrandAfterHooks
from tests import brand_dto_generator, RepoEnum, get_auth_user_event


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
        user_payload_arg: User = captor.arg
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
