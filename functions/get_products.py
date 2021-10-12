try:
    from web.functions.legacy_get_products import get_products
except:
    from layers.python.web.functions.legacy_get_products import get_products

def lambda_handler(event, context):
    return get_products(event, context)