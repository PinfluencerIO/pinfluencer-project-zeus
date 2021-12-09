from src.data_access_layer import image_repository
from src.data_access_layer.brand import Brand, brand_from_dict
from src.data_access_layer.product import product_from_dict, Product
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


def write_new_product(product_dict, brand_id, data_manager: DataManagerInterface):
    try:
        image_bytes = product_dict['image']
        product_dict['image'] = None
        product_dict['brand_id'] = brand_id
        product_entity = product_from_dict(product_dict)
        data_manager.session.add(product_entity)
        data_manager.session.flush()
        image_id = s3_image_repository.upload(f'{brand_id}/{product_entity.id}', image_bytes)
        print(f'loaded product {product_entity}')
        product_entity.image = image_id
        print(f'loaded product {product_entity}')
        data_manager.session.flush()
        data_manager.session.commit()
        return product_entity
    except Exception as e:
        print(f'Failed to write_new_product {e}')
        data_manager.session.rollback()
        raise e


def update_new_product(brand_id, product_id, product_as_dict, data_manager: DataManagerInterface):
    product = data_manager.session.query(Product).filter((Product.brand_id == brand_id),
                                                         (Product.id == product_id)).first()
    print(f'product loaded: {product}')
    print(f'product payload: {product_as_dict}')
    if product:
        product.name = product_as_dict['name']
        product.description = product_as_dict['description']
        product.requirements = product_as_dict['requirements']
        data_manager.session.flush()
        data_manager.session.commit()
        return product
    else:
        return None


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


def patch_product_image(brand_id, product_id, image_bytes, data_manager: DataManagerInterface):
    try:
        print(f'load product with id {product_id} and brand id {brand_id}')
        product = data_manager.session.query(Product).filter((Product.brand_id == brand_id),
                                                             (Product.id == product_id)).first()
        print(f'product loaded: {product}')
        if product:
            image_id = s3_image_repository.upload(f'{brand_id}/{product.id}', image_bytes)
            s3_image_repository.delete(f'{brand_id}/{product.image}')
            product.image = image_id
            data_manager.session.flush()
            data_manager.session.commit()
            return product
        else:
            return None
    except Exception as e:
        print(f'Failed to update product image {e}')
        data_manager.session.rollback()
        raise e


def delete_product(brand_id, product_id, data_manager):
    try:
        product: Product = (data_manager.session
                            .query(Product)
                            .filter(Product.id == product_id, Product.brand_id == brand_id)
                            .first())
        # TODO: This isn't atomic:
        # If delete image works, but delete product fails, we have lost the image, and rollback is partial
        if product:
            s3_image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
            data_manager.session.delete(product)
            data_manager.session.commit()
            return product
        else:
            return None
    except Exception as e:
        print(f'Failed to delete product {e}')
        data_manager.session.rollback()
        raise e
