import json

from jsonschema.exceptions import ValidationError

from src.crosscutting import print_exception
from src.data.repositories import AlreadyExistsException
from src.domain.models import ValueEnum, CategoryEnum, Brand
from src.web import PinfluencerResponse, get_cognito_user, BRAND_ID_PATH_KEY
from src.web.validation import valid_path_resource_id


class BrandController:
    def __init__(self, brand_repository, brand_validator):
        self.__brand_validator = brand_validator
        self.__brand_repository = brand_repository

    def get_all(self, event):
        return PinfluencerResponse(status_code=200, body=list(map(lambda x: x.__dict__,
                                                                  self.__brand_repository.load_collection())))

    def get_by_id(self, event):
        id_ = valid_path_resource_id(event, BRAND_ID_PATH_KEY)
        if id_:
            brand = self.__brand_repository.load_by_id(id_=id_)
            if brand:
                return PinfluencerResponse(status_code=200, body=brand.__dict__)
            return PinfluencerResponse(status_code=404, body={})
        return PinfluencerResponse(status_code=400, body={})

    def get(self, event):
        auth_user_id = get_cognito_user(event)
        if auth_user_id:
            brand = self.__brand_repository.load_for_auth_user(auth_user_id=auth_user_id)
            if brand:
                return PinfluencerResponse(status_code=200, body=brand.__dict__)
        return PinfluencerResponse(status_code=404, body={})

    def create(self, event):
        auth_user_id = get_cognito_user(event)
        payload_json_string = event['body']
        payload_dict = json.loads(payload_json_string)
        try:
            self.__brand_validator.validate(payload=payload_dict)
            brand = Brand(first_name=payload_dict["first_name"],
                          last_name=payload_dict["last_name"],
                          email=payload_dict["email"],
                          name=payload_dict["name"],
                          description=payload_dict["description"],
                          website=payload_dict["website"],
                          values=list(map(lambda x: ValueEnum[x], payload_dict["values"])),
                          categories=list(map(lambda x: CategoryEnum[x], payload_dict["categories"])))
            self.__brand_repository.write_new_for_auth_user(auth_user_id=auth_user_id, payload=brand)
        except (AlreadyExistsException, ValidationError) as e:
            print_exception(e)
            return PinfluencerResponse(status_code=400, body={})
        return PinfluencerResponse(status_code=201, body=brand.__dict__)

    def update(self, event):
        raise NotImplemented

    def update_header_image(self, event):
        raise NotImplemented

    def update_logo(self, event):
        raise NotImplemented
