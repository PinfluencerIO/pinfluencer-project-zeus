from src.data_access_layer import image_repository
from src.data_access_layer.brand import Brand, brand_from_dict
from src.interfaces.data_manager_interface import DataManagerInterface

s3_image_repository = image_repository.S3ImageRepository()


def write_new_brand(brand_as_dict, image_bytes, data_manager: DataManagerInterface):
    try:
        brand = brand_from_dict(brand_as_dict)
        data_manager.session.add(brand)
        data_manager.session.flush()
        image_id = s3_image_repository.upload(f'{brand.id}', image_bytes)
        brand: Brand = data_manager.session.query(Brand).filter(Brand.id == brand.id).first()
        brand.image = image_id
        data_manager.session.flush()
        data_manager.session.commit()
        return brand
    except Exception as e:
        print(f'Failed to write_new_brand {e}')
        data_manager.session.rollback()
        raise e


def update_brand(brand_id, brand_as_dict, data_manager: DataManagerInterface):
    print('write data access.update brand')
    print(f'brandId: {brand_id}')
    print(f'brand_dict: {brand_as_dict}')
    try:
        brand: Brand = data_manager.session.query(Brand).filter(Brand.id == brand_id).first()
        brand.name = brand_as_dict['name']
        brand.description = brand_as_dict['description']
        brand.website = brand_as_dict['website']
        brand.instahandle = brand_as_dict['instahandle']
        data_manager.session.flush()
        data_manager.session.commit()
        return brand
    except Exception as e:
        print(f'Failed to update_brand {e}')
        data_manager.session.rollback()
        raise e


def update_brand_image(brand_id, image_bytes, data_manager: DataManagerInterface):
    try:
        brand: Brand = data_manager.session.query(Brand).filter(Brand.id == brand_id).first()
        image_id = s3_image_repository.upload(f'{brand.id}', image_bytes)
        s3_image_repository.delete(f'{brand.id}/{brand.image}')
        brand.image = image_id
        data_manager.session.flush()
        data_manager.session.commit()
        return brand
    except Exception as e:
        print(f'Failed to update brand image {e}')
        data_manager.session.rollback()
        raise e
