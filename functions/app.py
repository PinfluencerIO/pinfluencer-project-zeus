import utils.util_web as web
import utils.util_log as log


def lambda_handler(event, context):
    response = web.Controller.process(event)
    log.logger.info("response: %s" % response)
    return response