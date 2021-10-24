import base64
import datetime
import json
import uuid

import boto3

s3 = boto3.client('s3')

from functions.processors.hacks.old_manual_db import execute_query, format_records, build_json_from_db_records, \
    find_brand_by_auth_user

COLUMNS_FOR_PRODUCT = ['id', 'name', 'description', 'image', 'requirements', 'brand_id', 'brand_name']
COLUMNS_FOR_PRODUCT_WITHOUT_IMAGE = ['id', 'name', 'description', 'requirements', 'brand_id', 'brand_name']
COLUMNS_FOR_BRAND = ['id', 'name', 'description', 'website', 'email', 'image', 'auth_user_id']
COLUMNS_FOR_BRAND_WITHOUT_IMAGE = ['id', 'name', 'description', 'website', 'email', 'auth_user_id']


def hack_get_brands(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand"
    result = execute_query(sql, None)
    records = format_records(result['records'])
    return build_json_from_db_records(records, COLUMNS_FOR_BRAND)


def hack_get_brand_by_id(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where id = :id"
    id_ = event['pathParameters']['brand_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result) == 0:
        return {}
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_BRAND)[0]


def hack_get_all_products_for_brand_by_id(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product where brand_id = :id"
    id_ = event['pathParameters']['brand_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_PRODUCT)


def hack_get_products(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product"
    result = execute_query(sql, None)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_PRODUCT)


def hack_get_product_by_id(event):
    cols = ', '.join(COLUMNS_FOR_PRODUCT)
    sql = "SELECT " + cols + " FROM product where id = :id"
    id_ = event['pathParameters']['product_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)

    c = COLUMNS_FOR_PRODUCT.copy()

    records = format_records(result['records'])
    if len(records) == 0:
        return {}
    else:
        return build_json_from_db_records(records, c)[0]


def hack_brand_me(event):
    cols = COLUMNS_FOR_BRAND
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    sql = "SELECT " + ', '.join(cols) + " FROM brand where auth_user_id = :id"
    parameter = [{'name': 'id', 'value': {'stringValue': user}}]
    result = execute_query(sql, parameter)
    body = format_records(result['records'])
    return build_json_from_db_records(body, cols)[0]


def hack_product_me_by_id(event):
    brand = hack_brand_me(event)
    product = hack_get_product_by_id(event)
    if brand['id'] != product['brand_id']:
        return {"message": "Unauthorised get"}
    else:
        return product


def hack_product_me(event):
    records, user = find_brand_by_auth_user(event)

    if len(records['records']) == 0:
        print(f"zero found for {user}")
        return {
            'statusCode': 200,
            'body': "no products"
        }

    id = format_records(records['records'])[0][0]
    second_sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product WHERE brand_id=:id"
    second_p = [{'name': 'id', 'value': {'stringValue': id}}]
    result = execute_query(second_sql, second_p)
    body = format_records(result['records'])
    return build_json_from_db_records(body, COLUMNS_FOR_PRODUCT)


def hack_brand_me_update(event):
    brand = hack_brand_me(event)
    body = json.loads(event['body'])
    email = get_email(body, event)
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

        return hack_brand_me(event)
    else:
        return {'message': 'failed to update brand'}


def hack_product_me_update(event):
    brand = hack_brand_me(event)
    product = hack_get_product_by_id(event)
    if brand['id'] != product['brand_id']:
        return {"message": "Update not allowed."}

    body = json.loads(event['body'])
    sql = "\
    UPDATE product \
        SET name = :name,\
            description = :description,\
            image = :image,\
            requirements = :requirements\
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
        return hack_get_product_by_id(event)
    else:
        return {'message': 'failed to update brand'}


def hack_brand_me_create(event):
    result, user = find_brand_by_auth_user(event)
    if len(result['records']) >= 1:
        return {'message': 'this user is already associated with a brand',
                'id': format_records(result['records'])[0][0]}
    else:
        id_ = str(uuid.uuid4())
        body = json.loads(event['body'])

        email = get_email(body, event)

        if has_image(body):
            cols = " ,".join(COLUMNS_FOR_BRAND)
        else:
            cols = ' ,'.join(COLUMNS_FOR_BRAND_WITHOUT_IMAGE)

        sql = "INSERT INTO brand(" + cols + ", created) " \
                                            "VALUES (:id, :name, :bio, :description, :website, :email, " \
              + with_image(body) + ":auth_user_id, :created)"
        sql_parameters = [
            {'name': 'id', 'value': {'stringValue': id_}},
            {'name': 'name', 'value': {'stringValue': body['name']}},
            {'name': 'bio', 'value': {'stringValue': body['description']}},
            {'name': 'description', 'value': {'stringValue': body['description']}},
            {'name': 'website', 'value': {'stringValue': body['website']}},
            {'name': 'email', 'value': {'stringValue': email}},
            {'name': 'auth_user_id', 'value': {'stringValue': user}},
            {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
        ]

        if has_image(body):
            sql_parameters.append({'name': 'image', 'value': {'stringValue': body['image']['filename']}})

        query_results = execute_query(sql, sql_parameters)
        if query_results['numberOfRecordsUpdated'] == 1:
            if has_image(body):
                upload_image_to_s3(id_, None, body['image']['filename'],body['image']['bytes'])
            return {'id': f'{id_}'}
        else:
            return {'message': 'failed to create brand'}


def hack_product_me_create(event):
    results, user = find_brand_by_auth_user(event)
    formatted_records = format_records(results['records'])
    brand_id = formatted_records[0][0]
    brand_name = formatted_records[0][1]
    body = json.loads(event['body'])
    if has_image(body):
        cols = ",".join(COLUMNS_FOR_PRODUCT)
    else:
        cols = ",".join(COLUMNS_FOR_PRODUCT_WITHOUT_IMAGE)
    sql = " \
        INSERT INTO product \
        (" + cols + ", created) \
        VALUES \
        (:id, :name, :description, " + with_image(body) + " :requirements, :brand_id, :brand_name, :created) \
    "
    id_ = str(uuid.uuid4())
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': id_}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'brand_id', 'value': {'stringValue': brand_id}},
        {'name': 'brand_name', 'value': {'stringValue': brand_name}},
        {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
        {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
    ]

    if has_image(body):
        sql_parameters.append({'name': 'image', 'value': {'stringValue': body['image']['filename']}})

    results = execute_query(sql, sql_parameters)
    if results['numberOfRecordsUpdated'] == 1:
        filename_ = body["image"]["filename"]
        bytes_ = body['image']['bytes']
        upload_image_to_s3(brand_id, id_, filename_, bytes_)

        return {'id': f'{id_}'}
    else:
        return {'message': 'failed to create product'}


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


def with_image(body):
    if has_image(body):
        return ":image, "
    else:
        return ""


def has_image(body):
    return 'image' in body and 'filename' in body['image']


def get_email(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        email = event['requestContext']['authorizer']['jwt']['claims']['email']
    else:
        email = body['email']
    return email


def hack_product_me_delete(event):
    brand = hack_brand_me(event)
    product = hack_get_product_by_id(event)

    if len(product) == 0:
        return {}

    if brand['id'] != product['brand_id']:
        return {"message": "Update not allowed."}

    results = execute_query("DELETE FROM product where id=:id",
                            [{'name': 'id', 'value': {'stringValue': product['id']}}])

    if results['numberOfRecordsUpdated'] == 1:
        return {'message': 'product deleted'}
    else:
        return {'message': 'failed to delete product'}


def hack_feed(event):
    single = {"id": "4f9cf273-f37f-44db-be0c-a081fd200a01",
              "created": "2021-10-18 17:24:22.644158",
              "name": "Product Name 1",
              "description": "Lorem ipsum dolor sit amet, Product 1",
              "image": "product_image_1.png",
              "brand": {"id": "4f9cf273-f37f-44db-be0c-a081fd209991",
                        "name": "Brand name 1"}
              }

    product_number = 1
    brand_number = 1
    result = []
    for i in range(20):
        item = single.copy()
        item_b = single['brand'].copy()
        item['id'] = f'{product_number}_{brand_number}'
        item['name'] = f'Product {product_number}_{brand_number}'
        item['description'] = f'This is the description for product {product_number}_{brand_number}'
        item["image"] = f'product_image_{product_number}_{brand_number}.png'
        item_b['id'] = f'{brand_number}'
        item_b['name'] = f'Brand {brand_number}'
        item['brand'] = item_b
        result.append(item)
        product_number = product_number + 1
        if product_number > 3:
            product_number = 1
            brand_number = brand_number + 1

    return result
