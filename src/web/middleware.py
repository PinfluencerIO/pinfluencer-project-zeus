import inspect

from src._types import Logger
from src.web import PinfluencerContext, PinfluencerSequenceBuilder


class MiddlewarePipeline:

    def __init__(self, logger: Logger):
        self.__logger = logger

    def execute_middleware(self, context: PinfluencerContext,
                           sequence: PinfluencerSequenceBuilder):
        middleware = sequence.generate_sequence()
        for action in middleware:
            name = "anonymous"
            try:
                name = f"{inspect.getmodule(action).__name__}.{action.__name__}"
            except Exception:
                ...
            self.__logger.log_debug(f"begin middleware {name}")
            self.__logger.log_trace(f"request {context.body}")
            self.__logger.log_trace(f"response {context.response.body}")
            action(context)
            if any(context.error_capsule):
                error = context.error_capsule[-1]
                self.__logger.log_error(f"error found in error capsule {type(error).__name__}")
                context.short_circuit = True
                context.response.body = {"message": error.message}
                context.response.status_code = error.status
            self.__logger.log_debug(f"end middleware {name}")
            if context.short_circuit:
                self.__logger.log_error(f"middleware SHORTED!")
                break
