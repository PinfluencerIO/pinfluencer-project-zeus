from typing import Callable

from jsonschema.exceptions import ValidationError

from src.crosscutting import print_exception
from src.domain.models import ValueEnum, CategoryEnum, Brand, Influencer
from src.domain.validation import InfluencerValidator
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import BrandRepository, Deserializer, BrandValidatable, UserRepository, InfluencerRepository
from src.web import PinfluencerResponse, BRAND_ID_PATH_KEY, INFLUENCER_ID_PATH_KEY, PinfluencerContext
from src.web.validation import valid_path_resource_id


class BaseUserController:

    def __init__(self,
                 user_repository: UserRepository,
                 resource_id: str):
        self._resource_id = resource_id
        self._user_repository = user_repository

    def _update_image(self, context: PinfluencerContext, updater: Callable[[str, str], dict]) -> [PinfluencerResponse,
                                                                                                  bool]:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            user = updater(auth_user_id, payload_dict['image_bytes'])
            return [PinfluencerResponse(status_code=200,
                                        body=user), False]
        except NotFoundException as e:
            print_exception(e)
            return [PinfluencerResponse(status_code=404, body={}), True]

    def get_all(self, context: PinfluencerContext) -> None:
        users = self._user_repository.load_collection()
        context.response.status_code = 200
        context.response.body = list(map(lambda x: x.__dict__, users))

    def get_by_id(self, context: PinfluencerContext) -> None:
        id_ = valid_path_resource_id(context.event, self._resource_id)
        if id_:
            try:
                user = self._user_repository.load_by_id(id_=id_)
                context.response.status_code = 200
                context.response.body = user.__dict__
                return
            except NotFoundException as e:
                print_exception(e)
                context.short_circuit = True
                context.response.status_code = 404
                context.response.body = {}
                return
        context.short_circuit = True
        context.response.status_code = 400
        context.response.body = {}

    def get(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        if auth_user_id:
            try:
                brand = self._user_repository.load_for_auth_user(auth_user_id=auth_user_id)
                context.response.status_code = 200
                context.response.body = brand.__dict__
                return
            except NotFoundException as e:
                print_exception(e)
        context.short_circuit = True
        context.response.status_code = 404
        context.response.body = {}


class BrandController(BaseUserController):
    def __init__(self, brand_repository: BrandRepository,
                 brand_validator: BrandValidatable,
                 deserializer: Deserializer):
        super().__init__(brand_repository, BRAND_ID_PATH_KEY)
        self.__brand_validator = brand_validator

    def create(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
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
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        context.response.body = brand.__dict__
        context.response.status_code = 201

    def update(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            self.__brand_validator.validate_brand(payload_dict)
            brand = Brand(brand_name=payload_dict["brand_name"],
                          brand_description=payload_dict["brand_description"],
                          website=payload_dict["website"],
                          insta_handle=payload_dict["insta_handle"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            brand_to_return = self._user_repository.update_for_auth_user(auth_user_id=auth_user_id, payload=brand)
            context.response.body = brand_to_return.__dict__
            context.response.status_code = 200
            return
        except ValidationError as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        except NotFoundException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 404

    def update_logo(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._user_repository.update_logo_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__)
        context.short_circuit = short_circuit
        context.response.body = response.body
        context.response.status_code = response.status_code

    def update_header_image(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._user_repository.update_header_image_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body


class InfluencerController(BaseUserController):

    def __init__(self, deserializer: Deserializer,
                 influencer_repository: InfluencerRepository,
                 influencer_validator: InfluencerValidator):
        super().__init__(influencer_repository, INFLUENCER_ID_PATH_KEY)
        self.__influencer_validator = influencer_validator

    def create(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
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
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
            return
        context.response.body = influencer.__dict__
        context.response.status_code = 201

    def update_profile_image(self, context: PinfluencerContext) -> None:
        [response, short_circuit] = self._update_image(context=context,
                                                       updater=lambda auth_id,
                                                                      bytes: self._user_repository.update_image_for_auth_user(
                                                           auth_id,
                                                           bytes).__dict__)
        context.short_circuit = short_circuit
        context.response.status_code = response.status_code
        context.response.body = response.body

    def update(self, context: PinfluencerContext) -> None:
        auth_user_id = context.auth_user_id
        payload_dict = context.body
        try:
            self.__influencer_validator.validate_influencer(payload_dict)
            influencer_from_db = self._user_repository.update_for_auth_user(auth_user_id=auth_user_id,
                                                                            payload=Influencer(
                                                                                auth_user_id=auth_user_id,
                                                                                insta_handle=payload_dict[
                                                                                    'insta_handle'],
                                                                                website=payload_dict["website"],
                                                                                bio=payload_dict["bio"],
                                                                                audience_male_split=payload_dict[
                                                                                    "audience_male_split"],
                                                                                audience_female_split=payload_dict[
                                                                                    "audience_female_split"],
                                                                                audience_age_13_to_17_split=
                                                                                payload_dict[
                                                                                    "audience_age_13_to_17_split"],
                                                                                audience_age_18_to_24_split=
                                                                                payload_dict[
                                                                                    "audience_age_18_to_24_split"],
                                                                                audience_age_25_to_34_split=
                                                                                payload_dict[
                                                                                    "audience_age_25_to_34_split"],
                                                                                audience_age_35_to_44_split=
                                                                                payload_dict[
                                                                                    "audience_age_35_to_44_split"],
                                                                                audience_age_45_to_54_split=
                                                                                payload_dict[
                                                                                    "audience_age_45_to_54_split"],
                                                                                audience_age_55_to_64_split=
                                                                                payload_dict[
                                                                                    "audience_age_55_to_64_split"],
                                                                                audience_age_65_plus_split=payload_dict[
                                                                                    "audience_age_65_plus_split"],
                                                                                values=list(map(lambda x: ValueEnum[x],
                                                                                                payload_dict[
                                                                                                    "values"])),
                                                                                categories=list(
                                                                                    map(lambda x: CategoryEnum[x],
                                                                                        payload_dict["categories"]))
                                                                            ))
            context.response.status_code = 200
            context.response.body = influencer_from_db.__dict__
            return
        except NotFoundException as e:
            print_exception(e)
            context.short_circuit = True
            context.response.status_code = 404
            context.response.body = {}
            return
        except ValidationError as e:
            print_exception(e)
            context.short_circuit = True
            context.response.status_code = 400
            context.response.body = {}
