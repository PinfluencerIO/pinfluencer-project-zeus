from src.web import PinfluencerContext, PinfluencerAction


class MiddlewarePipeline:

    def execute_middleware(self, context: PinfluencerContext,
                           middleware: list[PinfluencerAction]):
        for action in middleware:
            action(context)
            if context.short_circuit:
                break