from .util_web import Controller
from .util_log import logger


def lambda_handler(event, context):
    response = Controller.process(event)
    logger.info("response: %s" % response)
    return response