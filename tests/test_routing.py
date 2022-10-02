from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.app import logger_factory
from src.web import PinfluencerContext, PinfluencerResponse, ErrorCapsule, FluentSequenceBuilder
from src.web.middleware import MiddlewarePipeline


class DummyErrorCapsule(ErrorCapsule):

    def __init__(self):
        self.message = "im a teapot"
        self.status = 418


class TestMiddlewarePipeline(TestCase):

    def setUp(self) -> None:
        self.__sut = MiddlewarePipeline(logger=Mock())

    def test_execute(self):
        # arrange
        context = PinfluencerContext(body={
            "invocations": [

            ]
        }, short_circuit=False, response=PinfluencerResponse())
        middlware = [MagicMock(side_effect=lambda x: x.body["invocations"].append(1)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(2)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(3)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(4)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(5))]

        # act
        self.__sut.execute_middleware(context=context,
                                      middleware=middlware)

        # assert
        assert context.body["invocations"] == [1, 2, 3, 4, 5]

    @staticmethod
    def __short_middlware_with_error_capsule(context: PinfluencerContext, invoc_num: int):
        context.error_capsule.append(DummyErrorCapsule())
        context.body["invocations"].append(invoc_num)


    @staticmethod
    def __short_middlware(context: PinfluencerContext, invoc_num: int):
        context.short_circuit = True
        context.body["invocations"].append(invoc_num)

    def test_execute_and_middlware_shorts(self):
        # arrange
        context = PinfluencerContext(body={
            "invocations": [

            ]
        }, short_circuit=False, response=PinfluencerResponse())
        middlware = [MagicMock(side_effect=lambda x: x.body["invocations"].append(1)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(2)),
                     MagicMock(side_effect=lambda x: self.__short_middlware(context=x, invoc_num=3)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(4)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(5))]

        # act
        self.__sut.execute_middleware(context=context,
                                      middleware=middlware)

        # assert
        assert context.body["invocations"] == [1, 2, 3]


    def test_execute_and_middlware_shorts_when_error_capsules_are_appended_to(self):
        # arrange
        context = PinfluencerContext(body={
            "invocations": [

            ]
        }, short_circuit=False, response=PinfluencerResponse())
        middlware = [MagicMock(side_effect=lambda x: x.body["invocations"].append(1)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(2)),
                     MagicMock(side_effect=lambda x: self.__short_middlware_with_error_capsule(context=x, invoc_num=3)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(4)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(5))]

        # act
        self.__sut.execute_middleware(context=context,
                                      middleware=middlware)

        # assert
        with self.subTest(msg="invocation match sequence"):
            self.assertEqual(context.body["invocations"], [1, 2, 3])

        # assert
        with self.subTest(msg="body displays custom error message"):
            self.assertEqual(context.response.body, {"message": "im a teapot"})

        # assert
        with self.subTest(msg="body displays custom error code"):
            self.assertEqual(context.response.status_code, 418)



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
        self.add_command(self.__context.run4)\
            .add_command(self.__context.run5)\
            .add_command(self.__context.run6)


class DummyNestedSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, sequence: DummyNested2SequenceBuilder):
        super().__init__()
        self.__sequence = sequence

    def build(self):
        self._add_sequence(self.__sequence)


class DummySequenceBuilder(FluentSequenceBuilder):

    def __init__(self, context: CommandContextClass, sequence: DummyNestedSequenceBuilder):
        super().__init__()
        self.__sequence = sequence
        self.__context = context

    def build(self):
        self.add_command(self.__context.run1)\
            ._add_sequence(self.__sequence)\
            .add_command(self.__context.run2)\
            .add_command(self.__context.run3)


class TestSequenceBuilder(TestCase):

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
