from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.image_repository import S3ImageRepository
from src.filters.authorised_filter import GetBrandAssociatedWithCognitoUser
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.filters.valid_id_filters import LoadResourceById
from src.web.request_status_manager import RequestStatusManager


class Container:
    data_manager: DataManagerInterface
    image_repository: ImageRepositoryInterface
    get_brand_associated_with_cognito_user: GetBrandAssociatedWithCognitoUser
    valid_brand_filter: LoadResourceById
    valid_product_filter: LoadResourceById
    status_manager: RequestStatusManager

    def __init__(self):
        print("new container constructed")
        self.status_manager = RequestStatusManager()
        self.data_manager = DataManager(self.status_manager)
        self.image_repository = S3ImageRepository()
        self.get_brand_associated_with_cognito_user = GetBrandAssociatedWithCognitoUser(self.data_manager)
        self.valid_brand_filter = LoadResourceById(self.data_manager, 'brand')
        self.valid_product_filter = LoadResourceById(self.data_manager, 'product')
