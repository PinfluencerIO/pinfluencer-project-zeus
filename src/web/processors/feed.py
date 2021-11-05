from src.data_access_layer.product import Product
from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.processors import ProcessInterface
from src.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        self.__data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        brands: list[Brand] = self.__data_manager.session.query(Brand.id).limit(20).all()
        products = []
        for brand in brands:
            products.extend(self.__data_manager.session
                            .query(Product)
                            .filter(Product.brand_id == brand.id)
                            .limit(3)
                            .all())
        limitedProducts = products[:20]
        productsDict = []
        for product in limitedProducts:
            productsDict.append(product.as_dict())
        return PinfluencerResponse(body=productsDict)
