try:
    from web.controllers import legacy_product_controller as product_controller
except NameError:
    import layers.python.web.controllers.legacy_product_controller as product_controller

def handler(event, context):
    print("testing")
    return product_controller.post_products(event, context)