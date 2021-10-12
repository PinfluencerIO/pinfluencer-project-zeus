try:
    import web.controllers.legacy_brand_controller as brand_controller
    import web.controllers.legacy_product_controller as product_controller
except:
    import layers.python.web.controllers.legacy_brand_controller as brand_controller
    import layers.python.web.controllers.legacy_product_controller as product_controller

def get_brands_handler(event, context):
    return brand_controller.get_brands(event, context)

def post_brands_handler(event, context):
    return brand_controller.post_brands(event, context)

def get_products_handler(event, context):
    return product_controller.get_products(event, context)

def post_products_handler(event, context):
    return product_controller.post_products(event, context)