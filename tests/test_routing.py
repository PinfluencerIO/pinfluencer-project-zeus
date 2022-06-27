from unittest import TestCase
from unittest.mock import MagicMock

from src.web import PinfluencerContext
from src.web.middleware import MiddlewarePipeline


class TestMiddlewarePipeline(TestCase):

    def setUp(self) -> None:
        self.__sut = MiddlewarePipeline()

    def test_execute(self):
        # arrange
        context = PinfluencerContext(body={
            "invocations": [

            ]
        }, short_circuit=False)
        middlware = [MagicMock(side_effect=lambda x: x.body["invocations"].append(1)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(2)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(3)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(4)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(5))]

        # act
        self.__sut.execute_middleware(context=context,
                                      middleware=middlware)

        # assert
        print(context.body["invocations"])
        assert context.body["invocations"] == [1, 2, 3, 4, 5]

    @staticmethod
    def __short_middlware(context: PinfluencerContext, invoc_num: int):
        context.short_circuit = True
        context.body["invocations"].append(invoc_num)

    def test_execute_and_middlware_shorts(self):
        # arrange
        context = PinfluencerContext(body={
            "invocations": [

            ]
        }, short_circuit=False)
        middlware = [MagicMock(side_effect=lambda x: x.body["invocations"].append(1)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(2)),
                     MagicMock(side_effect=lambda x: self.__short_middlware(context=x, invoc_num=3)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(4)),
                     MagicMock(side_effect=lambda x: x.body["invocations"].append(5))]

        # act
        self.__sut.execute_middleware(context=context,
                                      middleware=middlware)

        # assert
        print(context.body["invocations"])
        assert context.body["invocations"] == [1, 2, 3]