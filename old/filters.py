import abc


class FilterChain:
    @abc.abstractmethod
    def do_filter(self, event: dict):
        pass


class FilterInterface:
    @abc.abstractmethod
    def do_filter(self, event: dict, filter_chain: FilterChain):
        pass


class FilterChainImp(FilterChain):
    def __init__(self, filters: list[FilterInterface]):
        self.filter_iterator = iter(filters)

    def do_filter(self, event: dict):
        try:
            next(self.filter_iterator).do_filter(event, self)
        except Exception as e:
            print(e)
            pass


class AuthFilter(FilterInterface):
    def do_filter(self, event: dict, filter_chain: FilterChain):
        if self._extract_authorizer(event) is None:
            raise Exception('Missing authorizer')
        else:
            filter_chain.do_filter(event)

    def _extract_authorizer(self, event):
        return None if 'authorizer' not in event['requestContext'] else event['requestContext']['authorizer']
