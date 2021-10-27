from src.processors.hacks.old_manual_db import COLUMNS_FOR_BRAND, execute_query, format_records, \
    build_json_for_brand


def select_brand_by_id(id_) -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where id = :id"
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    if len(result is None or result['records']) == 0:
        return []
    else:
        records = format_records(result['records'])
        return build_json_for_brand(records)


def select_brand_by_auth_user_id(auth_user_id) -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where auth_user_id = :auth_user_id"
    sql_parameters = [{'name': 'auth_user_id', 'value': {'stringValue': auth_user_id}}]
    result = execute_query(sql, sql_parameters)
    print(f'select brand by auth records len = {len(result["records"])}')
    if result is None or len(result['records']) == 0:
        print('return empty records')
        return []
    else:
        records = format_records(result['records'])
        return build_json_for_brand(records)


def select_all_brands() -> list[dict]:
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand"
    result = execute_query(sql, None)
    records = format_records(result['records'])
    return build_json_for_brand(records)
