import uuid

# Validates the id against the UUID v4 standard
def validId(id):
    try:
        val = uuid.UUID(id, version=4)
        
        # If the uuid_string is a valid hex code, 
        # but an invalid uuid4,
        # the UUID.__init__ will convert it to a 
        # valid uuid4. This is bad for validation purposes.
        # Therefore, try and match str with UUID
        if str(val) == id:
            pass
        else:
            raise Exception('Invalid UUID v 4')
    except Exception as e:
        raise InvalidId(f"{id} is not a valid UUID {e}")

class InvalidId(Exception):
    """Raised when id is not a UUID"""
    pass