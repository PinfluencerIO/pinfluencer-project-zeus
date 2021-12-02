from src.filters.payload_validation import *


def test_valid_put_brand_payload_response_200():
    filter_ = BrandPutPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Brand Name',
        'description': 'Brand Description',
        'website': 'https://www.brand.com',
        'email': 'person@brand.com',
        'instahandle': 'handle'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_put_brand_payload_response_400():
    filter_ = BrandPutPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'description': 'Brand Description',
        'website': 'https://www.brand.com',
        'email': 'person@brand.com',
        'instahandle': 'handle'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_valid_patch_brand_image_payload_response_200():
    filter_ = BrandImagePatchPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'image': 'bytes'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_patch_brand_image_payload_response_400():
    filter_ = BrandImagePatchPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'image-bytes': 'bytes'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_valid_post_brand_payload_response_200():
    filter_ = BrandPostPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Brand Name',
        'description': 'Brand Description',
        'website': 'https://www.brand.com',
        'email': 'person@brand.com',
        'instahandle': 'handle',
        'image': 'bytes'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_post_brand_payload_response_400():
    filter_ = BrandPostPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Brand Name',
        'description': 'Brand Description',
        'website': 'https://www.brand.com',
        'email': 'person@brand.com',
        'instahandle': 'handle'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_valid_post_product_payload_response_200():
    filter_ = ProductPostPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Product Name',
        'description': 'Product Description',
        'requirements': 'requirement, requirement',
        'image': 'bytes'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_post_product_payload_response_400():
    filter_ = ProductPostPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Product Name',
        'description': 'Product Description',
        'requirements': 'requirement, requirement'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_valid_put_product_payload_response_200():
    filter_ = ProductPutPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Product Name',
        'description': 'Product Description',
        'requirements': 'requirement, requirement'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_put_product_payload_response_400():
    filter_ = ProductPutPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'name': 'Product Name',
        'description': 'Product Description'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_valid_patch_product_image_payload_response_200():
    filter_ = ProductImagePatchPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'image': 'bytes'
    })})
    assert response.is_success() is True
    assert response.get_code() == 200


def test_invalid_patch_product_image_payload_response_400():
    filter_ = ProductImagePatchPayloadValidation()
    response = filter_.do_filter({'body': json.dumps({
        'image-bytes': 'bytes'
    })})
    assert response.is_success() is False
    assert response.get_code() == 400
