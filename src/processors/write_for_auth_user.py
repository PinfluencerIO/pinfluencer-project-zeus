import json

from jsonschema import validate

from src.data_access_layer.write_data_access import NoBrandForAuthenticatedUser, NotFoundException, \
    AlreadyExistsException
from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id, types, protect_email_from_update_if_held_in_claims, get_cognito_user


# TODO This really breaks the idea of a configurable generic write class. Talk to Aidan about this one
class ProcessWriteForAuthenticatedUser:
    def __init__(self, type_: str, action: str, db_write, data_manager) -> None:
        super().__init__()
        self.type_ = type_
        self.action = action
        self.db_write = db_write
        self.data_manager = data_manager

    def do_process(self, event):
        body_ = event["body"]
        payload = json.loads(body_)
        auth_user_id = get_cognito_user(event)
        protect_email_from_update_if_held_in_claims(payload, event)

        try:
            resource = self.db_write(auth_user_id, payload, self.data_manager)
            print(f'updated {resource}')
            return PinfluencerResponse(201, resource.as_dict()) \
                if self.action == 'post' else PinfluencerResponse(200, resource.as_dict())
        except NoBrandForAuthenticatedUser as no_brand:
            return PinfluencerResponse.as_400_error()
        except NotFoundException as nfe:
            return PinfluencerResponse(404, str(nfe))
        except AlreadyExistsException as aee:
            # TODO See class level todo: Generic class with specific business rule exception?
            return PinfluencerResponse.as_400_error('Brand already associated with auth user')


class ProcessWriteWithValidationForAuthenticatedUser(ProcessWriteForAuthenticatedUser):
    def do_process(self, event):
        print('With Validation')
        body_ = event["body"]
        payload = json.loads(body_)
        try:
            print(f"validator: {types[self.type_][self.action]['validator']}")
            validate(instance=payload, schema=(types[self.type_][self.action]['validator']))
            return super().do_process(event)
        except Exception as e:
            print(f'Failed post payload schema validation {e}')
            return PinfluencerResponse.as_400_error('Invalid post payload')


class ProcessWriteForAuthenticatedUserWithProductId(ProcessWriteWithValidationForAuthenticatedUser):
    def do_process(self, event):
        print('With product_id')
        body_ = event["body"]
        payload = json.loads(body_)
        resource_id = valid_path_resource_id(event, types[self.type_]['key'])
        if resource_id is None:
            return PinfluencerResponse.as_400_error(f'{self} Invalid path parameter id')
        else:
            payload['product_id'] = resource_id
            event["body"] = json.dumps(payload)
            print(f'adding product id to payload {event["body"]}')
            return super().do_process(event)
