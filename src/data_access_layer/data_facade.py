import json

from src.data_access_layer.alchemy_encoder import new_alchemy_encoder
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.repositories.alchemy_brand_repository import AlchemyBrandRepository
from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository

data_manager = DataManager()
brand_repository = AlchemyBrandRepository(data_manager=data_manager)
product_repository = AlchemyProductRepository(data_manager=data_manager)
# product_repository.create(data=ProductModel(name="prod1", description="this is a desc", requirements="blah,blah,blah", image="testimage", brand_id="d2e44a78-b955-4f9b-a411-88904dc4b364"))
brands = brand_repository.readall()
for brand in brands:
    brandDict = json.dumps(brand, cls=new_alchemy_encoder(), check_circular=False, indent=4)
    print(brandDict)
print("")
products = product_repository.readall()
for brand in brands:
    brandDict = json.dumps(brand, cls=new_alchemy_encoder(), check_circular=False, indent=4)
    print(brandDict)
print("")