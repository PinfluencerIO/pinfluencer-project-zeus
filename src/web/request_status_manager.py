class RequestStatusManager:
    __status: bool = False

    @property
    def status(self) -> bool:
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__status = value
