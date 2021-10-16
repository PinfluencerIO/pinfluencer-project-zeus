try:
    from utils import util_web, util_log
except Exception as e:
    print(e)


def lambda_handler(event, context):
    response = util_web.Controller.process(event)
    util_log.logger.info("response: %s" % response)
    return response