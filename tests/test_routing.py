from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.web import PinfluencerContext, PinfluencerResponse, ErrorCapsule
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
