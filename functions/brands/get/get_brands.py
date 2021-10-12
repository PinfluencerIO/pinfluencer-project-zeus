try:
    from web.lambda_layer.legacy_get_brands import get_brands
except:
    from layers.python.web.lambda_layer.legacy_get_brands import get_brands

def lambda_handler(event, context):
    return get_brands(event, context);