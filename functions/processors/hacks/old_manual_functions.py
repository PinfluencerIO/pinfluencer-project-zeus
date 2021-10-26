import base64
import datetime
import json
import uuid
import boto3

from functions.processors.hacks import brand_helps, product_helps
from functions.processors.hacks.brand_helps import select_brand_by_auth_user_id
from functions.processors.hacks.old_manual_db import execute_query, \
    COLUMNS_FOR_BRAND, COLUMNS_FOR_PRODUCT, PRODUCT_TEMPLATE, build_json_for_brand, build_json_for_product, \
    format_records
from functions.processors.hacks.product_helps import select_product_by_id
from functions.web.http_util import PinfluencerResponse

s3 = boto3.client('s3')


def get_feed(event):
    product_number = 1
    brand_number = 1
    result = []
    for i in range(20):
        item = PRODUCT_TEMPLATE.copy()
        item_b = PRODUCT_TEMPLATE['brand'].copy()
        item_i = PRODUCT_TEMPLATE['image'].copy()
        item['id'] = f'{product_number}_{brand_number}'
        item['name'] = f'Product {product_number}_{brand_number}'
        item['description'] = f'This is the description for product {product_number}_{brand_number}'
        item_i['filename'] = f'product_image_{product_number}_{brand_number}.png'
        item_b['id'] = f'{brand_number}'
        item_b['name'] = f'Brand {brand_number}'
        item['brand'] = item_b
        item['image'] = item_i
        result.append(item)
        product_number = product_number + 1
        if product_number > 3:
            product_number = 1
            brand_number = brand_number + 1

    return PinfluencerResponse(body=result)


def get_all_brands(event) -> PinfluencerResponse:
    return PinfluencerResponse(body=brand_helps.select_all_brands())


def get_brand_by_id(event) -> PinfluencerResponse:
    return PinfluencerResponse(body=event['brand'])


def get_all_products_for_brand_with_id(event):
    brand = event['brand']
    products = product_helps.select_all_products_for_brand_with_id(brand['id'])
    return PinfluencerResponse(body=products)


def get_all_products(event):
    return PinfluencerResponse(body=product_helps.select_all_products())


def get_product_by_id(event) -> PinfluencerResponse:
    return PinfluencerResponse(body=event['product'])


#
# def hack_brand_me(event):
#     user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
#     sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where auth_user_id = :id"
#     parameter = [{'name': 'id', 'value': {'stringValue': user}}]
#     result = execute_query(sql, parameter)
#     if len(result[0]) == 0:
#         return PinfluencerResponse(status_code=404, body={})
#     else:
#         records = format_records(result['records'])
#         formatted_as_json = build_json_for_brand(records)
#         return PinfluencerResponse(status_code=200, body=formatted_as_json)
#
#
# def hack_product_me_by_id(event):
#     brand = hack_brand_me(event)
#     if brand.status_code == 404:
#         return PinfluencerResponse(status_code=404, body={'message': 'failed to find brand'})
#     else:
#         product = hack_get_product_by_id(event)
#         if product.status_code == 404:
#             return PinfluencerResponse(status_code=404, body={
#                 'message': f'failed to find product associated with brand {brand.body["id"]}'})
#         else:
#             return product
#
#
# def hack_product_me(event):
#     records, user = find_brand_by_auth_user(event)
#
#     if len(records['records']) == 0:
#         return PinfluencerResponse(status_code=404, body={})
#
#     id_ = format_records(records['records'])[0][0]
#     second_sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product WHERE brand_id=:id"
#     second_p = [{'name': 'id', 'value': {'stringValue': id_}}]
#     result = execute_query(second_sql, second_p)
#     if len(result[0]) == 0:
#         return PinfluencerResponse(status_code=404, body={})
#     else:
#         records = format_records(result['records'])
#         return PinfluencerResponse(status_code=200, body=build_json_for_product(records))
#
#
# def hack_brand_me_update(event):
#     brand = hack_brand_me(event)
#     print(f'brand lookup {brand}')
#     if brand.status_code == 404:
#         return brand
#     print(f'body\n{event["body"]}')
#     body = json.loads(event['body'])
#     email = get_email(body, event)
#     sql = "\
#     UPDATE brand \
#         SET name = :name,\
#             description = :description,\
#             website = :website,\
#             email = :email,\
#             image = :image\
#         WHERE id = :id\
#     "
#     sql_parameters = [
#         {'name': 'id', 'value': {'stringValue': brand.body['id']}},
#         {'name': 'name', 'value': {'stringValue': body['name']}},
#         {'name': 'description', 'value': {'stringValue': body['description']}},
#         {'name': 'website', 'value': {'stringValue': body['website']}},
#         {'name': 'email', 'value': {'stringValue': email}},
#         {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
#     ]
#     query_results = execute_query(sql, sql_parameters)
#
#     if query_results['numberOfRecordsUpdated'] == 1:
#         upload_image_to_s3(brand.body['id'], None, body['image']['filename'], body['image']['bytes'])
#
#         return hack_brand_me(event)
#     else:
#         return PinfluencerResponse(status_code=400, body={"message": "Failed to update brand"})
#
#
# def hack_product_me_update(event):
#     brand = hack_brand_me(event)
#     if brand.status_code == 404:
#         return brand
#     product = hack_get_product_by_id(event)
#     if product.status_code == 404:
#         return product
#
#     if brand.body['id'] != product.body['brand_id']:
#         return PinfluencerResponse(status_code=401, body={"message": "Not allowed to update this product"})
#
#     body = json.loads(event['body'])
#     sql = "\
#     UPDATE product \
#         SET name = :name,\
#             description = :description,\
#             image = :image,\
#             requirements = :requirements\
#         WHERE id = :id\
#     "
#     sql_parameters = [
#         {'name': 'id', 'value': {'stringValue': product.body['id']}},
#         {'name': 'name', 'value': {'stringValue': body['name']}},
#         {'name': 'description', 'value': {'stringValue': body['description']}},
#         {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
#         {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
#     ]
#     query_results = execute_query(sql, sql_parameters)
#
#     if query_results['numberOfRecordsUpdated'] == 1:
#         upload_image_to_s3(brand.body['id'], product.body['id'], body['image']['filename'], body['image']['bytes'])
#         return hack_get_product_by_id(event)
#     else:
#         return PinfluencerResponse(status_code=400, body={'message': 'failed to update product'})


def get_user(event):
    return event['requestContext']['authorizer']['jwt']['claims']['cognito:username']


def hack_brand_me_update(event):
    body = json.loads(event['body'])
    email = get_email(body, event)
    brand = event['auth_brand']
    sql = "\
        UPDATE brand \
            SET name = :name,\
                description = :description,\
                website = :website,\
                email = :email,\
                image = :image\
            WHERE id = :id\
        "
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': brand['id']}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'website', 'value': {'stringValue': body['website']}},
        {'name': 'email', 'value': {'stringValue': email}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
    ]
    query_results = execute_query(sql, sql_parameters)
    if query_results['numberOfRecordsUpdated'] == 1:
        upload_image_to_s3(brand['id'], None, body['image']['filename'], body['image']['bytes'])
        updated_brand = select_brand_by_auth_user_id(get_user(event))
        return PinfluencerResponse(body=updated_brand)
    else:
        return PinfluencerResponse.as_500_error('Failed update brand')


def hack_brand_me_create(event):
    body = json.loads(event['body'])
    id_ = str(uuid.uuid4())
    email = get_email(body, event)
    user = get_user(event)
    sql = "INSERT INTO brand(" + " ,".join(COLUMNS_FOR_BRAND) + ") " \
                                                                "VALUES (:id, :name, :description, :website, :email, :image, :auth_user_id, :created)"

    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': id_}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'website', 'value': {'stringValue': body['website']}},
        {'name': 'email', 'value': {'stringValue': email}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
        {'name': 'auth_user_id', 'value': {'stringValue': user}},
        {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
    ]
    query_results = execute_query(sql, sql_parameters)
    if query_results['numberOfRecordsUpdated'] == 1:
        upload_image_to_s3(id_, None, body['image']['filename'], body['image']['bytes'])
        new_brand = select_brand_by_auth_user_id(user)
        return PinfluencerResponse(body=new_brand)
    else:
        return PinfluencerResponse.as_500_error('Failed to create brand')


def hack_product_me(event):
    brand = event['auth_brand']
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product WHERE brand_id=:id"
    parameters = [{'name': 'id', 'value': {'stringValue': brand['id']}}]
    query_results = execute_query(sql, parameters)
    records = format_records(query_results['records'])
    return PinfluencerResponse(body=build_json_for_product(records))


def hack_product_me_create(event):
    body = json.loads(event['body'])
    brand = event['auth_brand']
    sql = " \
        INSERT INTO product \
        (" + ",".join(COLUMNS_FOR_PRODUCT) + ") \
        VALUES \
        (:id, :name, :description, :requirements, :image, :brand_id, :brand_name, :created)"

    id_ = str(uuid.uuid4())

    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': id_}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'brand_id', 'value': {'stringValue': brand['id']}},
        {'name': 'brand_name', 'value': {'stringValue': brand['name']}},
        {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
        {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
    ]

    query_results = execute_query(sql, sql_parameters)
    if query_results['numberOfRecordsUpdated'] == 1:
        upload_image_to_s3(brand['id'], id_, body['image']['filename'], body['image']['bytes'])
        new_product = select_product_by_id(id_)
        return PinfluencerResponse(body=new_product)
    else:
        return PinfluencerResponse.as_500_error('Failed to create product')


def hack_product_me_update(event):
    body = json.loads(event['body'])
    brand = event['auth_brand']
    product = event['product']
    sql = "\
            UPDATE product \
                SET name = :name,\
                    description = :description,\
                    requirements = :requirements,\
                    image = :image\
                WHERE id = :id\
            "

    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': product['id']}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
    ]

    query_results = execute_query(sql, sql_parameters)
    if query_results['numberOfRecordsUpdated'] == 1:
        upload_image_to_s3(brand['id'], product['id'], body['image']['filename'], body['image']['bytes'])
        updated_product = select_product_by_id(product['id'])
        return PinfluencerResponse(body=updated_product)
    else:
        return PinfluencerResponse.as_500_error('Failed to create product')


#
# def hack_product_me_create(event):
#     brand = hack_brand_me(event)
#     if brand.status_code == 404:
#         return brand
#
#     # results, user = find_brand_by_auth_user(event)
#     # formatted_records = format_records(results['records'])
#     # brand_id = formatted_records[0][0]
#     # brand_name = formatted_records[0][1]
#     body = json.loads(event['body'])
#
#     sql = " \
#         INSERT INTO product \
#         (" + ",".join(COLUMNS_FOR_PRODUCT) + ", created) \
#         VALUES \
#         (:id, :name, :description, :requirements, :image, :brand_id, :brand_name, :created) \
#     "
#     id_ = str(uuid.uuid4())
#     sql_parameters = [
#         {'name': 'id', 'value': {'stringValue': id_}},
#         {'name': 'name', 'value': {'stringValue': body['name']}},
#         {'name': 'description', 'value': {'stringValue': body['description']}},
#         {'name': 'brand_id', 'value': {'stringValue': brand.body['id']}},
#         {'name': 'brand_name', 'value': {'stringValue': brand.body['name']}},
#         {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
#         {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
#         {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
#     ]
#
#     results = execute_query(sql, sql_parameters)
#     if results['numberOfRecordsUpdated'] == 1:
#         filename_ = body["image"]["filename"]
#         bytes_ = body['image']['bytes']
#         upload_image_to_s3(brand.body['id'], id_, filename_, bytes_)
#
#         return PinfluencerResponse(status_code=201, body={"id": f"{id_}"})
#     else:
#         return PinfluencerResponse(status_code=400, body={'message': 'failed to create product'})


# Todo: When implementing this again in OO, use SQS so failures can be mitigated
def upload_image_to_s3(brand_id, product_id_, filename_, bytes_):
    print(f'brand{brand_id}, product{product_id_}, fn{filename_}')
    image = base64.b64decode(bytes_)
    if product_id_ is None:
        key = f'{brand_id}/{filename_}'
    else:
        key = f'{brand_id}/{product_id_}/{filename_}'
    s3.put_object(Bucket='pinfluencer-product-images',
                  Key=key, Body=image,
                  ContentType=f'image/{filename_[-3:]}',
                  Tagging='public=yes')


# def with_image(body):
#     if has_image(body):
#         return ":image, "
#     else:
#         return ""
#
#
# def has_image(body):
#     return 'image' in body and 'filename' in body['image']


def get_email(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        email = event['requestContext']['authorizer']['jwt']['claims']['email']
    else:
        email = body['email']
    return email


def delete_product(event):
    results = execute_query("DELETE FROM product WHERE id=:id",
                            [{'name': 'id', 'value': {'stringValue': event['product']['id']}}])
    if results['numberOfRecordsUpdated'] == 1:
        return PinfluencerResponse(status_code=200, body={"message": f"Product {event['product']['id']} deleted"})
    else:
        return PinfluencerResponse(status_code=500, body={"message": f"Failed to delete product {event['product']['id']}"})


# def hack_product_me_delete(event):
#     brand = hack_brand_me(event)
#     if brand.status_code == 400:
#         return brand
#
#     product = hack_get_product_by_id(event)
#     if product.status_code == 400:
#         return product
#
#     if brand.body['id'] != product.body['brand_id']:
#         return PinfluencerResponse(status_code=401, body={"message": "Not allowed to delete this product"})
#
#     results = execute_query("DELETE FROM product where id=:id",
#                             [{'name': 'id', 'value': {'stringValue': product.body['id']}}])
#
#     if results['numberOfRecordsUpdated'] == 1:
#         return PinfluencerResponse(status_code=200, body={"message": "Deleted this product"})
#     else:
#         return PinfluencerResponse(status_code=200, body={"message": "Failed to delete this product"})
#
