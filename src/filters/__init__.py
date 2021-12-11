class FilterResponse:
    def __init__(self, message: str, code: int, payload: dict):
        self._message = message
        self.__code = code
        self.__payload = payload

    def is_success(self):
        return 200 >= self.__code < 300

    def get_message(self):
        return self._message

    def get_code(self):
        return self.__code

    def get_payload(self):
        return self.__payload
