import datetime
import json
import uuid

from functions.processors.hacks.old_manual_db import execute_query, format_records, build_json_from_db_records, \
    find_brand_by_auth_user

COLUMNS_FOR_PRODUCT = ['id', 'name', 'description', 'image', 'requirements', 'brand_id', 'brand_name']
COLUMNS_FOR_PRODUCT_WITHOUT_IMAGE = ['id', 'name', 'description', 'requirements', 'brand_id', 'brand_name']
COLUMNS_FOR_BRAND = ['id', 'name', 'bio', 'description', 'website', 'email', 'image', 'auth_user_id']
COLUMNS_FOR_BRAND_WITHOUT_IMAGE = ['id', 'name', 'bio', 'description', 'website', 'email', 'auth_user_id']
COLUMNS_FOR_BRAND_WITH_VERSION = \
    ['id', 'name', 'bio', 'description', 'website', 'email', 'image', 'auth_user_id', 'version']


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


def hack_get_product_by_id(event, with_version=False):
    if with_version:
        cols = ', '.join(COLUMNS_FOR_PRODUCT) + ', version'
    else:
        cols = ', '.join(COLUMNS_FOR_PRODUCT)
    sql = "SELECT " + cols + " FROM product where id = :id"
    id_ = event['pathParameters']['product_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)

    c = COLUMNS_FOR_PRODUCT.copy()
    if with_version:
        c.append('version')

    records = format_records(result['records'])
    if len(records) == 0:
        return {}
    else:
        return build_json_from_db_records(records, c)[0]


def hack_brand_me(event, with_version=False):
    if with_version:
        cols = COLUMNS_FOR_BRAND_WITH_VERSION
    else:
        cols = COLUMNS_FOR_BRAND
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    sql = "SELECT " + ', '.join(cols) + " FROM brand where auth_user_id = :id"
    parameter = [{'name': 'id', 'value': {'stringValue': user}}]
    result = execute_query(sql, parameter)
    body = format_records(result['records'])
    return build_json_from_db_records(body, cols)[0]


def hack_product_me_by_id(event):
    brand = hack_brand_me(event)
    product = hack_get_product_by_id(event, True)
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
    brand = hack_brand_me(event, True)
    version = brand['version'] + 1
    body = json.loads(event['body'])
    email = get_email(body, event)
    sql = "\
    UPDATE brand \
        SET name = :name,\
            bio = :bio,\
            description = :description,\
            website = :website,\
            email = :email,\
            image = :image,\
            version = :version\
        WHERE id = :id\
    "
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': brand['id']}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'bio', 'value': {'stringValue': body['bio']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'website', 'value': {'stringValue': body['website']}},
        {'name': 'email', 'value': {'stringValue': email}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
        {'name': 'version', 'value': {'longValue': version}}
    ]
    query_results = execute_query(sql, sql_parameters)

    if query_results['numberOfRecordsUpdated'] == 1:
        return hack_brand_me(event)
    else:
        return {'message': 'failed to update brand'}


def hack_product_me_update(event):
    brand = hack_brand_me(event)
    product = hack_get_product_by_id(event, True)
    if brand['id'] != product['brand_id']:
        return {"message": "Update not allowed."}

    version = product['version']
    body = json.loads(event['body'])
    sql = "\
    UPDATE product \
        SET name = :name,\
            description = :description,\
            image = :image,\
            requirements = :requirements,\
            version = :version\
        WHERE id = :id\
    "
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': product['id']}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'description', 'value': {'stringValue': body['description']}},
        {'name': 'requirements', 'value': {'stringValue': body['requirements']}},
        {'name': 'image', 'value': {'stringValue': body['image']['filename']}},
        {'name': 'version', 'value': {'longValue': version+1}}
    ]
    query_results = execute_query(sql, sql_parameters)

    if query_results['numberOfRecordsUpdated'] == 1:
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

        sql = "INSERT INTO brand(" + cols + ", created, version) " \
              "VALUES (:id, :name, :bio, :description, :website, :email, " \
              + with_image(body) + ":auth_user_id, :created, :version)"
        sql_parameters = [
            {'name': 'id', 'value': {'stringValue': id_}},
            {'name': 'name', 'value': {'stringValue': body['name']}},
            {'name': 'bio', 'value': {'stringValue': body['description']}},
            {'name': 'description', 'value': {'stringValue': body['description']}},
            {'name': 'website', 'value': {'stringValue': body['website']}},
            {'name': 'email', 'value': {'stringValue': email}},
            {'name': 'auth_user_id', 'value': {'stringValue': user}},
            {'name': 'created', 'value': {'stringValue': str(datetime.datetime.utcnow())}},
            {'name': 'version', 'value': {'longValue': 1}}
        ]

        if has_image(body):
            sql_parameters.append({'name': 'image', 'value': {'stringValue': body['image']['filename']}})

        query_results = execute_query(sql, sql_parameters)
        if query_results['numberOfRecordsUpdated'] == 1:
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
        (" + cols + ", created, version) \
        VALUES \
        (:id, :name, :description, " + with_image(body) + " :requirements, :brand_id, :brand_name, :created, :version) \
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
        {'name': 'version', 'value': {'longValue': 1}}
    ]

    if has_image(body):
        sql_parameters.append({'name': 'image', 'value': {'stringValue': body['image']['filename']}})

    results = execute_query(sql, sql_parameters)
    if results['numberOfRecordsUpdated'] == 1:
        return {'id': f'{id_}'}
    else:
        return {'message': 'failed to create product'}


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
    product = hack_get_product_by_id(event, True)

    if len(product) == 0:
        return {}

    if brand['id'] != product['brand_id']:
        return {"message": "Update not allowed."}

    results = execute_query("DELETE FROM product where id=:id", [{'name': 'id', 'value': {'stringValue': product['id']}}])

    if results['numberOfRecordsUpdated'] == 1:
        return {'message': 'product deleted'}
    else:
        return {'message': 'failed to delete product'}
