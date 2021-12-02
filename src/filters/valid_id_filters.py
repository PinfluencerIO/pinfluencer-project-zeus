import uuid

from src import log_util
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.service_layer import load_by_id
from src.filters import FilterInterface, FilterResponse


class LoadResourceById(FilterInterface):
    __resources = {'brand': Brand, 'product': Product}

    def __init__(self, data_manager: DataManagerInterface, resource: str) -> None:
        self.__data_manager = data_manager
        self.resource = resource
        self.__resource_type = self.__resources[resource]
        self.__resource_key = resource + '_id'

    def do_filter(self, event: dict):
        try:
            id_ = event['pathParameters'][self.__resource_key]
        except KeyError:
            return FilterResponse(f'Missing key in event pathParameters.{self.__resource_key}', 400)

        if valid_uuid(id_):
            loaded_resource = load_by_id(id_, self.__resource_type, self.__data_manager)
            if loaded_resource is None:
                return FilterResponse(f'No {self.resource} found with id {id_}', 404)
            else:
                event[self.resource] = loaded_resource.as_dict()
                return FilterResponse('', 200)
        else:
            return FilterResponse(f'{id_} is invalid', 400)


def valid_uuid(id_):
    try:
        val = uuid.UUID(id_, version=4)
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            log_util.print_exception(f'equality failed {val} {id_}')
    except ValueError as ve:
        log_util.print_exception(ve)
    except AttributeError as e:
        log_util.print_exception(e)

    return False
