from typing import Callable

from jsonschema.exceptions import ValidationError

from src.crosscutting import print_exception
from src.domain.models import ValueEnum, CategoryEnum, Brand
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, Deserializer, BrandValidatable, UserRepository
from src.web import PinfluencerResponse, get_cognito_user, BRAND_ID_PATH_KEY
from src.web.validation import valid_path_resource_id


class BaseUserController:

    def __init__(self, serializer: Deserializer,
                 user_repository: UserRepository):
        self.__user_repository = user_repository
        self._deserializer = serializer

    def _update_image(self, event, updater: Callable[[str, str], dict]) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = self._deserializer.deserialize(payload_json_string)
        try:
            user = updater(auth_user_id, payload_dict['image_bytes'])
            return PinfluencerResponse(status_code=200,
                                       body=user)
        except NotFoundException as e:
            print_exception(e)
            return PinfluencerResponse(status_code=404, body={})

    def get_all(self, event) -> PinfluencerResponse:
        return PinfluencerResponse(status_code=200, body=list(map(lambda x: x.__dict__,
                                                                  self.__user_repository.load_collection())))

    def get_by_id(self, event) -> PinfluencerResponse:
        id_ = valid_path_resource_id(event, BRAND_ID_PATH_KEY)
        if id_:
            try:
                brand = self.__user_repository.load_by_id(id_=id_)
                return PinfluencerResponse(status_code=200, body=brand.__dict__)
            except NotFoundException as e:
                print_exception(e)
                return PinfluencerResponse(status_code=404, body={})
        return PinfluencerResponse(status_code=400, body={})

    def get(self, event) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        if auth_user_id:
            try:
                brand = self.__user_repository.load_for_auth_user(auth_user_id=auth_user_id)
                return PinfluencerResponse(status_code=200, body=brand.__dict__)
            except NotFoundException as e:
                print_exception(e)
        return PinfluencerResponse(status_code=404, body={})


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository,
                 brand_validator: BrandValidatable,
                 deserializer: Deserializer):
        super().__init__(deserializer, brand_repository)
        self.__brand_validator = brand_validator
        self.__brand_repository = brand_repository

    def create(self, event) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = self._deserializer.deserialize(payload_json_string)
        try:
            self.__brand_validator.validate_brand(payload=payload_dict)
            brand = Brand(first_name=payload_dict["first_name"],
                          last_name=payload_dict["last_name"],
                          email=payload_dict["email"],
                          brand_name=payload_dict["brand_name"],
                          brand_description=payload_dict["brand_description"],
                          website=payload_dict["website"],
                          insta_handle=payload_dict["insta_handle"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            self.__brand_repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=brand)
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        return PinfluencerResponse(status_code=201, body=brand.__dict__)

    def update(self, event) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = self._deserializer.deserialize(payload_json_string)
        try:
            self.__brand_validator.validate_brand(payload_dict)
            brand = Brand(first_name=payload_dict["first_name"],
                          last_name=payload_dict["last_name"],
                          email=payload_dict["email"],
                          brand_name=payload_dict["brand_name"],
                          brand_description=payload_dict["brand_description"],
                          website=payload_dict["website"],
                          insta_handle=payload_dict["insta_handle"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            brand_to_return = self.__brand_repository.update_for_auth_user(auth_user_id=auth_user_id, payload=brand)
            return PinfluencerResponse(status_code=200, body=brand_to_return.__dict__)
        except ValidationError as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        except NotFoundException as e:
            print_exception(e)
            return PinfluencerResponse(status_code=404, body={})

    def update_logo(self, event) -> PinfluencerResponse:
        return self._update_image(event=event,
                                  updater=lambda auth_id, bytes: self.__brand_repository.update_logo_for_auth_user(
                                                 auth_id,
                                                 bytes).__dict__)

    def update_header_image(self, event) -> PinfluencerResponse:
        return self._update_image(event=event,
                                  updater=lambda auth_id, bytes: self.__brand_repository.update_header_image_for_auth_user(
                                                 auth_id,
                                                 bytes).__dict__)

class InfluencerController(BaseUserController):

    def create(self, event) -> PinfluencerResponse:
        ...