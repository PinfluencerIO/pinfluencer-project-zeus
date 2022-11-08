from src.web import ErrorCapsule


class AudienceDataAlreadyExistsErrorCapsule(ErrorCapsule):

    def __init__(self, auth_user_id: str):
        self.message = f"audience data already exists for {auth_user_id}"
        self.status = 400
