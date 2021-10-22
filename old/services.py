import abc


class ResourceServiceInterface:
    @abc.abstractmethod
    def doit(self):
        pass



class BrandServiceImplementation(ResourceServiceInterface):
    def __init__(self, respository: RepositoryInterface):
        self._respository = respository

    def doit(self):
        print('do it from BrandServiceImp')