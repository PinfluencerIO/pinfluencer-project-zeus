from src.processors.hacks.old_manual_db import COLUMNS_FOR_PRODUCT, execute_query, format_records, \
    build_json_for_product


def select_all_products() -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product"
    result = execute_query(sql, None)
    records = format_records(result['records'])
    return build_json_for_product(records)


def select_product_by_id(id_) -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product where id = :id"
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result is None or result['records']) == 0:
        return []
    else:
        records = format_records(result['records'])
        return build_json_for_product(records)


def select_all_products_for_brand_with_id(id_) -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product where brand_id = :id"
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result is None or result['records']) == 0:
        return []
    else:
        records = format_records(result['records'])
        return build_json_for_product(records)
