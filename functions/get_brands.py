try:
    from web.functions.legacy_get_brands import get_brands
except:
    from layers.python.web.functions.legacy_get_brands import get_brands

def lambda_handler(event, context):
    return get_brands(event, context)