from src._types import Logger
from src.web import PinfluencerContext, PinfluencerAction


class MiddlewarePipeline:

    def __init__(self, logger: Logger):
        self.__logger = logger

    def execute_middleware(self, context: PinfluencerContext,
                           middleware: list[PinfluencerAction]):
        for action in middleware:
            name = "anonymous"
            try:
                name = action.__name__
            except Exception:
                ...
            self.__logger.log_debug(f"begin middleware {name}")
            self.__logger.log_trace(f"request {context.body}")
            self.__logger.log_trace(f"response {context.response.body}")
            action(context)
            self.__logger.log_debug(f"end middleware {name}")
            if context.short_circuit:
                self.__logger.log_error(f"middleware SHORTED!")
                break