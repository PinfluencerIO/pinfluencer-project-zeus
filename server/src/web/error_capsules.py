from src.web import ErrorCapsule


class AudienceDataAlreadyExistsErrorCapsule(ErrorCapsule):

    def __init__(self, auth_user_id: str):
        self.message = f"audience data already exists for {auth_user_id}"
        self.status = 400


class AudienceDataNotFoundErrorCapsule(ErrorCapsule):

    def __init__(self, type: str, auth_user_id: str):
        self.message = f"audience {type} data not found for {auth_user_id}"
        self.status = 404


class BrandNotFoundErrorCapsule(ErrorCapsule):

    def __init__(self, auth_user_id: str):
        self.message = f"brand {auth_user_id} not found"
        self.status = 404


class BrandNotAuthorized(ErrorCapsule):

    def __init__(self, auth_user_id: str):
        self.message = f"brand {auth_user_id} not authorized for this request"
        self.status = 401


class InfluencerNotFoundErrorCapsule(ErrorCapsule):

    def __init__(self, auth_user_id: str):
        self.message = f"influencer {auth_user_id} not found"
        self.status = 404


class ListingNotFoundErrorCapsule(ErrorCapsule):

    def __init__(self, id: str):
        self.message = f"listing {id} not found"
        self.status = 404
