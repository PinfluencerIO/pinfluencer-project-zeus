from functions import util_web


def lambda_handler(event, context):
    result = util_web.Controller.process(event)

    return result
