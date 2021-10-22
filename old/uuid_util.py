import uuid
from functions import log_util


def valid_uuid(id_):
    try:
        print(f'valid {id_}')
        val = uuid.UUID(id_, version=4)
        print(f'val {val}')
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            return False
    except ValueError:
        return False
    except AttributeError as e:
        log_util.print_exception(e)
