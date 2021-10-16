import util_web

def lambda_handler(event, context):
    response = util_web.Controller.process(event)
    print("response: %s" % response)
    return response