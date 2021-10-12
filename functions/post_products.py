try:
    from web.functions.legacy_post_products import post_products
except:
    from layers.python.web.functions.legacy_post_products import post_products

def lambda_handler(event, context):
    return post_products(event, context)