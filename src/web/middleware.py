from src.web import PinfluencerContext, PinfluencerAction


class MiddlewarePipeline:

    def execute_middleware(self, context: PinfluencerContext,
                           middleware: list[PinfluencerAction]):
        for action in middleware:
            print(f"begin middleware")
            action(context)
            print(f"end middleware")
            if context.short_circuit:
                print(f"middleware SHORTED!")
                break