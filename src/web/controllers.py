from typing import Callable

from jsonschema.exceptions import ValidationError

from src.crosscutting import print_exception
from src.domain.models import ValueEnum, CategoryEnum, Brand, Influencer
from src.domain.validation import InfluencerValidator
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, Deserializer, BrandValidatable, UserRepository, InfluencerRepository, \
    AuthUserRepository
from src.web import PinfluencerResponse, get_cognito_user, BRAND_ID_PATH_KEY, INFLUENCER_ID_PATH_KEY
from src.web.validation import valid_path_resource_id


class BaseUserController:

    def __init__(self, deserializer: Deserializer,
                 user_repository: UserRepository,
                 auth_user_repository: AuthUserRepository,
                 resource_id: str):
        self._resource_id = resource_id
        self._auth_user_repository = auth_user_repository
        self._user_repository = user_repository
        self._deserializer = deserializer

    def _update_image(self, event: dict, updater: Callable[[str, str], dict]) -> PinfluencerResponse:
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

    def get_all(self, event: dict) -> PinfluencerResponse:
        brands = self._user_repository.load_collection()
        for brand in brands:
            user = self._auth_user_repository.get_by_id(_id=brand.auth_user_id)
            brand.first_name = user.first_name
            brand.last_name = user.last_name
            brand.email = user.email
        return PinfluencerResponse(status_code=200, body=list(map(lambda x: x.__dict__, brands)))

    def get_by_id(self, event: dict) -> PinfluencerResponse:
        id_ = valid_path_resource_id(event, self._resource_id)
        if id_:
            try:
                user = self._user_repository.load_by_id(id_=id_)
                auth_user = self._auth_user_repository.get_by_id(_id=user.auth_user_id)
                user.first_name = auth_user.first_name
                user.last_name = auth_user.last_name
                user.email = auth_user.email
                return PinfluencerResponse(status_code=200, body=user.__dict__)
            except NotFoundException as e:
                print_exception(e)
                return PinfluencerResponse(status_code=404, body={})
        return PinfluencerResponse(status_code=400, body={})

    def get(self, event: dict) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        if auth_user_id:
            try:
                brand = self._user_repository.load_for_auth_user(auth_user_id=auth_user_id)
                user = self._auth_user_repository.get_by_id(_id=auth_user_id)
                brand.first_name = user.first_name
                brand.last_name = user.last_name
                brand.email = user.email
                return PinfluencerResponse(status_code=200, body=brand.__dict__)
            except NotFoundException as e:
                print_exception(e)
        return PinfluencerResponse(status_code=404, body={})


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository,
                 brand_validator: BrandValidatable,
                 deserializer: Deserializer,
                 auth_user_repository: AuthUserRepository):
        super().__init__(deserializer, brand_repository, auth_user_repository, BRAND_ID_PATH_KEY)
        self.__brand_validator = brand_validator

    def create(self, event: dict) -> PinfluencerResponse:
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
            self._user_repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=brand)
            self._auth_user_repository.update_brand_claims(user=brand)
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        return PinfluencerResponse(status_code=201, body=brand.__dict__)

    def update(self, event: dict) -> PinfluencerResponse:
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
            brand_to_return = self._user_repository.update_for_auth_user(auth_user_id=auth_user_id, payload=brand)
            auth_user = self._auth_user_repository.get_by_id(_id=auth_user_id)
            brand_to_return.first_name = auth_user.first_name
            brand_to_return.last_name = auth_user.last_name
            brand_to_return.email = auth_user.email
            return PinfluencerResponse(status_code=200, body=brand_to_return.__dict__)
        except ValidationError as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        except NotFoundException as e:
            print_exception(e)
            return PinfluencerResponse(status_code=404, body={})

    def update_logo(self, event: dict) -> PinfluencerResponse:
        return self._update_image(event=event,
                                  updater=lambda auth_id, bytes: self._user_repository.update_logo_for_auth_user(
                                      auth_id,
                                      bytes).__dict__)

    def update_header_image(self, event) -> PinfluencerResponse:
        return self._update_image(event=event,
                                  updater=lambda auth_id,
                                                 bytes: self._user_repository.update_header_image_for_auth_user(
                                      auth_id,
                                      bytes).__dict__)


class InfluencerController(BaseUserController):

    def __init__(self, deserializer: Deserializer,
                 influencer_repository: InfluencerRepository,
                 auth_user_repository: AuthUserRepository,
                 influencer_validator: InfluencerValidator):
        super().__init__(deserializer, influencer_repository, auth_user_repository, INFLUENCER_ID_PATH_KEY)
        self.__influencer_validator = influencer_validator

    def create(self, event: dict) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = self._deserializer.deserialize(payload_json_string)
        try:
            self.__influencer_validator.validate_influencer(payload=payload_dict)
            influencer = Influencer(first_name=payload_dict["first_name"],
                                    last_name=payload_dict["last_name"],
                                    email=payload_dict["email"],
                                    bio=payload_dict["bio"],
                                    website=payload_dict["website"],
                                    insta_handle=payload_dict["insta_handle"],
                                    values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                                    categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])),
                                    auth_user_id=auth_user_id,
                                    audience_male_split=payload_dict["audience_male_split"],
                                    audience_female_split=payload_dict["audience_female_split"],
                                    audience_age_13_to_17_split=payload_dict["audience_age_13_to_17_split"],
                                    audience_age_18_to_24_split=payload_dict["audience_age_18_to_24_split"],
                                    audience_age_25_to_34_split=payload_dict["audience_age_25_to_34_split"],
                                    audience_age_35_to_44_split=payload_dict["audience_age_35_to_44_split"],
                                    audience_age_45_to_54_split=payload_dict["audience_age_45_to_54_split"],
                                    audience_age_55_to_64_split=payload_dict["audience_age_55_to_64_split"],
                                    audience_age_65_plus_split=payload_dict["audience_age_65_plus_split"])
            self._user_repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=influencer)
            self._auth_user_repository.update_influencer_claims(user=influencer)
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        return PinfluencerResponse(status_code=201, body=influencer.__dict__)

    def update_profile_image(self, event: dict) -> PinfluencerResponse:
        return self._update_image(event=event,
                                  updater=lambda auth_id, bytes: self._user_repository.update_image_for_auth_user(
                                      auth_id,
                                      bytes).__dict__)

    def update(self, event: dict) -> PinfluencerResponse:
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = self._deserializer.deserialize(payload_json_string)
        try:
            self.__influencer_validator.validate_influencer(payload_dict)
            influencer_from_db = self._user_repository.update_for_auth_user(auth_user_id=auth_user_id,
                                                       payload=Influencer(
                                                           auth_user_id=auth_user_id,
                                                           insta_handle=payload_dict['insta_handle'],
                                                           website=payload_dict["website"],
                                                           bio=payload_dict["bio"],
                                                           audience_male_split=payload_dict["audience_male_split"],
                                                           audience_female_split=payload_dict["audience_female_split"],
                                                           audience_age_13_to_17_split=payload_dict["audience_age_13_to_17_split"],
                                                           audience_age_18_to_24_split=payload_dict["audience_age_18_to_24_split"],
                                                           audience_age_25_to_34_split=payload_dict["audience_age_25_to_34_split"],
                                                           audience_age_35_to_44_split=payload_dict["audience_age_35_to_44_split"],
                                                           audience_age_45_to_54_split=payload_dict["audience_age_45_to_54_split"],
                                                           audience_age_55_to_64_split=payload_dict["audience_age_55_to_64_split"],
                                                           audience_age_65_plus_split=payload_dict["audience_age_65_plus_split"],
                                                           values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                                                           categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"]))
                                                       ))
            auth_user = self._auth_user_repository.get_by_id(_id=auth_user_id)
            influencer_from_db.first_name = auth_user.first_name
            influencer_from_db.last_name = auth_user.last_name
            influencer_from_db.email = auth_user.email
            return PinfluencerResponse(status_code=200, body=influencer_from_db.__dict__)
        except NotFoundException as e:
            print_exception(e)
            return PinfluencerResponse(status_code=404, body={})
        except ValidationError as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
