import abc


class FilterChain:
    @abc.abstractmethod
    def do_chain(self, event):
        pass


class FilterInterface:
    @abc.abstractmethod
    def do_filter(self, event: dict):
        pass


class FilterChainImp(FilterChain):
    """
    Handles the chaining of calls through the FilterChain
    """

    def __init__(self, filters: list[FilterInterface]):
        self.filters = filters

    def do_chain(self, event: dict):
        for filter_ in self.filters:
            filter_.do_filter(event)
