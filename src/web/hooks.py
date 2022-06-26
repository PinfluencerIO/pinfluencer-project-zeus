from src.types import AuthUserRepository
from src.web import PinfluencerContext


class BrandAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository):
        self.__auth_user_repository = auth_user_repository

    def set_brand_claims(self, context: PinfluencerContext):
        ...


class InfluencerAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository):
        self.__auth_user_repository = auth_user_repository

    def set_influencer_claims(self, context: PinfluencerContext):
        ...


class UserBeforeHooks:

    def set_auth_user_id(self, context: PinfluencerContext):
        context.auth_user_id = context.event['requestContext']['authorizer']['jwt']['claims']['cognito:username']


class UserAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository):
        self.__auth_user_repository = auth_user_repository

    def tag_auth_user_claims_to_response(self, context: PinfluencerContext):
        auth_user = self.__auth_user_repository.get_by_id(_id=context.response.body["auth_user_id"])
        context.response.body["first_name"] = auth_user.first_name
        context.response.body["last_name"] = auth_user.last_name
        context.response.body["email"] = auth_user.email

    def tag_auth_user_claims_to_response_collection(self, context: PinfluencerContext):
        for user in context.response.body:
            auth_user = self.__auth_user_repository.get_by_id(_id=user["auth_user_id"])
            user["first_name"] = auth_user.first_name
            user["last_name"] = auth_user.last_name
            user["email"] = auth_user.email
