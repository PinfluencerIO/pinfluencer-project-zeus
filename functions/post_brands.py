try:
    from web.functions.legacy_post_brands import post_brands
except:
    from layers.python.web.functions.legacy_post_brands import post_brands

def lambda_handler(event, context):
    return post_brands(event, context)