import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def print_exception(e):
    logger.error(''.join(['Exception ', str(type(e))]))
    logger.error(''.join(['Exception ', str(e)]))