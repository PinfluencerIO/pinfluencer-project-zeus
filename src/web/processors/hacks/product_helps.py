from src.web.processors.hacks.old_manual_db import execute_query, format_records, PRODUCT_TEMPLATE


def select_all_products() -> list[dict]:
    sql = "SELECT product.id, " \
          "product.name, " \
          "product.description, " \
          "product.requirements, " \
          "product.created, " \
          "brand.id as \"brand_id\", " \
          "brand.name as \"brand_name\" " \
          "FROM product " \
          "INNER JOIN brand on product.brand_id = brand.id "
    result = execute_query(sql, None)
    records = format_records(result['records'])
    results = []
    for record in records:
        copy_product = PRODUCT_TEMPLATE.copy()
        copy_brand = PRODUCT_TEMPLATE['brand'].copy()
        copy_product['id'] = record[0]
        copy_product['name'] = record[1]
        copy_product['description'] = record[2]
        copy_product['requirements'] = record[3]
        copy_product['created'] = record[4]
        copy_brand['id'] = record[5]
        copy_brand['name'] = record[6]
        copy_product['brand'] = copy_brand
        results.append(copy_product)

    return results


def select_product_by_id(id_) -> list[dict]:
    sql = "SELECT product.id, " \
          "product.name, " \
          "product.description, " \
          "product.requirements, " \
          "product.created, " \
          "brand.id as \"brand_id\", " \
          "brand.name as \"brand_name\" " \
          "FROM product " \
          "INNER JOIN brand on brand.id = brand_id and product.id = :id"
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result is None or result['records']) == 0:
        return []
    else:
        records = format_records(result['records'])
        results = []
        for record in records:
            copy_product = PRODUCT_TEMPLATE.copy()
            copy_brand = PRODUCT_TEMPLATE['brand'].copy()
            copy_product['id'] = record[0]
            copy_product['name'] = record[1]
            copy_product['description'] = record[2]
            copy_product['requirements'] = record[3]
            copy_product['created'] = record[4]
            copy_brand['id'] = record[5]
            copy_brand['name'] = record[6]
            copy_product['brand'] = copy_brand
            results.append(copy_product)

        return results


def select_all_products_for_brand_with_id(id_) -> list[dict]:
    sql = "SELECT product.id, " \
          "product.name, " \
          "product.description, " \
          "product.requirements, " \
          "product.created, " \
          "brand.id as \"brand_id\", " \
          "brand.name as \"brand_name\" " \
          "FROM product " \
          "INNER JOIN brand on brand.id = brand_id and brand.id = :id"
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result is None or result['records']) == 0:
        return []
    else:
        records = format_records(result['records'])
        results = []
        for record in records:
            copy_product = PRODUCT_TEMPLATE.copy()
            copy_brand = PRODUCT_TEMPLATE['brand'].copy()
            copy_product['id'] = record[0]
            copy_product['name'] = record[1]
            copy_product['description'] = record[2]
            copy_product['requirements'] = record[3]
            copy_product['created'] = record[4]
            copy_brand['id'] = record[5]
            copy_brand['name'] = record[6]
            copy_product['brand'] = copy_brand
            results.append(copy_product)

        return results
