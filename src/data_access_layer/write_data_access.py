from src.data_access_layer.brand import Brand, brand_from_dict
from src.data_access_layer.image_repository import ImageException
from src.data_access_layer.product import product_from_dict, Product
from src.data_access_layer.read_data_access import load_brand_for_authenticated_user


# TODO Need a not found exception instead of return None
def db_write_new_brand_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    # There cannot be a brand associated with auth_user_id
    brand = load_brand_for_authenticated_user(auth_user_id, data_manager)
    if brand:
        raise AlreadyExistsException(f'Brand {brand.id} already associated with {auth_user_id}')
    else:
        try:
            payload['auth_user_id'] = auth_user_id
            brand = brand_from_dict(payload)
            data_manager.session.add(brand)
            data_manager.session.flush()
            image_id = image_repository.upload(f'{brand.id}', payload['image_bytes'])
            brand = data_manager.session.query(Brand).filter(Brand.id == brand.id).first()
            brand.image = image_id
            data_manager.session.flush()
            data_manager.session.commit()
            return brand
        except Exception as e:
            print(f'Failed to write_new_brand {e}')
            data_manager.session.rollback()
            raise e


def db_write_update_brand_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    try:
        brand = load_brand_for_authenticated_user(auth_user_id=auth_user_id, data_manager=data_manager)
        if brand is None:
            raise NoBrandForAuthenticatedUser()
        brand.name = payload['name']
        brand.description = payload['description']
        brand.website = payload['website']
        brand.instahandle = payload['instahandle']
        data_manager.session.flush()
        data_manager.session.commit()
        return brand
    except Exception as e:
        print(f'Failed to update_brand {e}')
        data_manager.session.rollback()
        raise e


def db_write_patch_brand_image_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    try:
        brand = load_brand_for_authenticated_user(auth_user_id=auth_user_id, data_manager=data_manager)
        if brand is None:
            raise NoBrandForAuthenticatedUser()
        image_id = image_repository.upload(f'{brand.id}', payload['image_bytes'])
        try:
            image_repository.delete(f'{brand.id}/{brand.image}')
        except ImageException:
            print(f'Failed to delete image {brand.id}/{brand.image}')
        brand.image = image_id
        data_manager.session.flush()
        data_manager.session.commit()
        return brand
    except Exception as e:
        print(f'Failed to update brand image {e}')
        data_manager.session.rollback()
        raise e


def db_write_new_product_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    try:
        brand = load_brand_for_authenticated_user(auth_user_id, data_manager)
        print(f'check auth has brand {brand} {type(brand)}')
        if brand is None:
            raise NoBrandForAuthenticatedUser()
        else:
            print(f'brand found..move to update product')
        print(f'payload: {payload}')
        payload['brand_id'] = brand.id
        product_entity = product_from_dict(payload)
        print(f'{product_entity}')
        data_manager.session.add(product_entity)
        data_manager.session.flush()
        image_id = image_repository.upload(f'{brand.id}/{product_entity.id}', payload['image_bytes'])
        product_entity.image = image_id
        data_manager.session.flush()
        data_manager.session.commit()
        return product_entity
    except Exception as e:
        print(f'Failed to write_new_product {e}')
        data_manager.session.rollback()
        raise e


def db_write_update_product_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    brand = load_brand_for_authenticated_user(auth_user_id, data_manager)
    if brand is None:
        raise NoBrandForAuthenticatedUser()

    product = data_manager.session.query(Product).filter((Product.brand_id == brand.id),
                                                         (Product.id == payload['product_id'])).first()
    print(f'load product for update {product}')
    if product:
        product.name = payload['name']
        product.description = payload['description']
        product.requirements = payload['requirements']
        data_manager.session.flush()
        data_manager.session.commit()
        return product
    else:
        raise NotFoundException(f'Product not found for id {payload["product_id"]}')


def db_write_patch_product_image_for_auth_user(auth_user_id, payload, data_manager, image_repository):
    brand = load_brand_for_authenticated_user(auth_user_id, data_manager)
    if brand is None:
        raise NoBrandForAuthenticatedUser()
    try:
        print(f'load product with id {payload["product_id"]} and brand id {brand.id}')
        product = data_manager.session.query(Product).join(Brand).filter(
            Product.brand_id == brand.id, Product.id == payload["product_id"]).first()
        print(f'product loaded: {product}')
        if product:
            image_id = image_repository.upload(f'{brand.id}/{product.id}', payload['image_bytes'])
            image_repository.delete(f'{brand.id}/{product.id}/{product.image}')
            product.image = image_id
            data_manager.session.flush()
            data_manager.session.commit()
            return product
        else:
            raise NotFoundException(f'Product {payload["product_id"]} brand {brand.id} not found')
    except NotFoundException as nfe:
        raise nfe
    except Exception as e:
        print(f'Failed to update product image {e}')
        data_manager.session.rollback()
        raise e


# TODO: This isn't atomic s3 succeeds but db failed, image is lost
def delete_product(auth_user_id, product_id, data_manager, image_repository):
    brand = load_brand_for_authenticated_user(auth_user_id, data_manager)
    if brand is None:
        raise NoBrandForAuthenticatedUser()

    try:
        product = (data_manager.session
                   .query(Product)
                   .filter(Product.id == product_id, Product.brand_id == brand.id)
                   .first())
        if product is None:
            raise NotFoundException(f'Product {product_id} for brand {brand.id} not found')

        image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
        data_manager.session.delete(product)
        data_manager.session.commit()
        return product
    except NotFoundException as nfe:
        raise nfe
    except Exception as e:
        print(f'Failed to delete product {e}')
        data_manager.session.rollback()
        raise e


class AlreadyExistsException(Exception):
    pass


class NoBrandForAuthenticatedUser(Exception):
    pass


class NotFoundException(Exception):
    pass
