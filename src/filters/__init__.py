import abc


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


class FilterChain:
    @abc.abstractmethod
    def do_chain(self, event) -> FilterResponse:
        pass


class FilterInterface:
    @abc.abstractmethod
    def do_filter(self, event: dict) -> FilterResponse:
        pass


class FilterChainImp(FilterChain):
    """
    Handles the chaining of calls through the FilterChain
    """

    def __init__(self, filters: list[FilterInterface]):
        self.filters = filters

    def do_chain(self, event: dict) -> FilterResponse:
        response = FilterResponse('', 200, {})
        for filter_ in self.filters:
            response = filter_.do_filter(event)
            if not response.is_success():
                return response

        return response
