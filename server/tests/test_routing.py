from unittest import TestCase

from src.app import logger_factory
from src.web import PinfluencerContext, PinfluencerResponse, ErrorCapsule, FluentSequenceBuilder
from src.web.middleware import MiddlewarePipeline


class DummyErrorCapsule(ErrorCapsule):

    def __init__(self):
        self.message = "im a teapot"
        self.status = 418


class DummyNestedErrorSequenceBuilder(FluentSequenceBuilder):

    @property
    def invocations(self) -> list[str]:
        return self.__invocations

    def __init__(self, type="no error"):
        super().__init__()
        self.__type = type
        self.__invocations = []

    def build(self):
        self._add_command(self.command1)\
            ._add_command(self.command2)\
            ._add_command(self.command3)

    def command1(self, context: PinfluencerContext):
        self.__invocations.append("run 1")
        if self.__type == "error capsule":
            context.error_capsule.append(DummyErrorCapsule())

    def command2(self, context: PinfluencerContext):
        self.__invocations.append("run 2")
        if self.__type == "short circuit":
            context.short_circuit = True
            context.response.body = {"hello": "world"}
            context.response.status_code = 400

    def command3(self, context: PinfluencerContext):
        self.__invocations.append("run 3")

class CommandContextClass:

    def __init__(self):
        self.__invocations: list[str] = []

    def run1(self, context: PinfluencerContext):
        self.__invocations.append("run1")

    def run2(self, context: PinfluencerContext):
        self.__invocations.append("run2")

    def run_invalid(self, value: str):
        ...


    def run3(self, context: PinfluencerContext):
        self.__invocations.append("run3")

    def run4(self, context: PinfluencerContext):
        self.__invocations.append("run4")

    def run5(self, context: PinfluencerContext):
        self.__invocations.append("run5")

    def run6(self, context: PinfluencerContext):
        self.__invocations.append("run6")

    @property
    def invocations(self) -> list[str]:
        return self.__invocations


class DummyNested2SequenceBuilder(FluentSequenceBuilder):

    def __init__(self, context: CommandContextClass):
        super().__init__()
        self.__context = context

    def build(self):
        self._add_command(self.__context.run4)\
            ._add_command(self.__context.run5)\
            ._add_command(self.__context.run6)


class DummyNestedSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, sequence: DummyNested2SequenceBuilder):
        super().__init__()
        self.__sequence = sequence

    def build(self):
        self._add_sequence_builder(self.__sequence)


class DummySequenceBuilder(FluentSequenceBuilder):

    def __init__(self, context: CommandContextClass, sequence: DummyNestedSequenceBuilder):
        super().__init__()
        self.__sequence = sequence
        self.__context = context

    def build(self):
        self._add_command(self.__context.run1)\
            ._add_sequence_builder(self.__sequence)\
            ._add_command(self.__context.run2)\
            ._add_command(self.__context.run3)


class TestSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        middleware = MiddlewarePipeline(logger=logger_factory())
        sut = DummyNestedErrorSequenceBuilder()

        # act
        middleware.execute_middleware(context=PinfluencerContext(response=PinfluencerResponse(), short_circuit=False),
                                      sequence=sut)

        # assert
        self.assertEqual(sut.invocations, ["run 1", "run 2", "run 3"])

    def test_sequence_with_short_circuit(self):
        # arrange
        middleware = MiddlewarePipeline(logger=logger_factory())
        sut = DummyNestedErrorSequenceBuilder(type="short circuit")
        context = PinfluencerContext(response=PinfluencerResponse(body={}),
                                     short_circuit=False)

        # act
        middleware.execute_middleware(context=context,
                                      sequence=sut)

        # assert
        with self.subTest("invocations match"):
            self.assertEqual(sut.invocations, ["run 1", "run 2"])

        # assert
        with self.subTest("context is updated"):
            self.assertEqual(context.response.body, {"hello": "world"})
            self.assertEqual(context.response.status_code, 400)

    def test_sequence_with_error_capsule(self):
        # arrange
        middleware = MiddlewarePipeline(logger=logger_factory())
        sut = DummyNestedErrorSequenceBuilder(type="error capsule")
        context = PinfluencerContext(response=PinfluencerResponse(),
                                     short_circuit=False)

        # act
        middleware.execute_middleware(context=context,
                                      sequence=sut)

        # assert
        with self.subTest("invocations match"):
            self.assertEqual(sut.invocations, ["run 1"])

        # assert
        with self.subTest("context is updated"):
            self.assertEqual(context.response.body, {"message": "im a teapot"})
            self.assertEqual(context.response.status_code, 418)


class TestComplexSequenceBuilder(TestCase):

    def setUp(self) -> None:
        self.__command_context = CommandContextClass()
        self.__sut = DummySequenceBuilder(context=self.__command_context,
                                          sequence=DummyNestedSequenceBuilder(
                                              sequence=DummyNested2SequenceBuilder(context=self.__command_context)))
        self.__middleware = MiddlewarePipeline(logger=logger_factory())

    def test_build_and_run_sequence(self):
        # act
        self.__middleware.execute_middleware(context=PinfluencerContext(response=PinfluencerResponse(),
                                                                        short_circuit=False),
                                             sequence=self.__sut)

        # assert
        with self.subTest(msg="invocations match list"):
            self.assertEqual(self.__command_context.invocations, ["run1", "run4", "run5", "run6", "run2", "run3"])
