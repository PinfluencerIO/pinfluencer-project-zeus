from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.domain.models import User
from src.types import AuthUserRepository
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.hooks import UserAfterHooks
from tests import brand_dto_generator, RepoEnum


class TestUserAfterHooks(TestCase):

    def setUp(self) -> None:
        self.__auth_user_repository: AuthUserRepository = Mock()
        self.__sut = UserAfterHooks(auth_user_repository=self.__auth_user_repository)

    def test_tag_auth_user_claims_to_response(self):

        # arrange
        brand = brand_dto_generator(num=1, repo=RepoEnum.STD_REPO)
        response = PinfluencerResponse(body=brand.__dict__)
        auth_user_id = "12341"
        auth_user = User(first_name="cognito_first_name",
                         last_name="cognito_last_name",
                         email="cognito_email")
        self.__auth_user_repository.get_by_id = MagicMock(return_value=auth_user)

        # act
        self.__sut.tag_auth_user_claims_to_response(context=PinfluencerContext(response=response,
                                                                               event={},
                                                                               auth_user_id=auth_user_id))

        # assert
        assert response.body["first_name"] == auth_user.first_name
        assert response.body["last_name"] == auth_user.last_name
        assert response.body["email"] == auth_user.email
        self.__auth_user_repository.get_by_id.assert_called_once_with(_id=auth_user_id)