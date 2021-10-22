import abc


class ProcessInterface:
    @abc.abstractmethod
    def do_process(self, event: dict):
        pass
