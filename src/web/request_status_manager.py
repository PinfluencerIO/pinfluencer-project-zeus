class RequestStatusManager:
    __status: bool

    def __init__(self):
        print("status manager constructed")
        self.__status = False

    @property
    def status(self) -> bool:
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__status = value
