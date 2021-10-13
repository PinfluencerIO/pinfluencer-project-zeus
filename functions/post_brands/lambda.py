try:
    from web.controllers import legacy_brand_controller as brand_controller
except NameError:
    import layers.python.web.controllers.legacy_brand_controller as brand_controller

def handler(event, context):
    print("testing")
    return brand_controller.post_brands(event, context)