from sys import _getframe
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.web import PinfluencerContext, PinfluencerResponse
from src.web.middleware import MiddlewarePipeline


def class_meta(frame):
    class_context = '__module__' in frame.f_locals
    assert class_context, 'Frame is not a class context'

    module_name = frame.f_locals['__module__']
    class_name = frame.f_code.co_name
    return module_name, class_name

def print_class_path():
    print('%s.%s' % class_meta(_getframe(1)))


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
        print(context.body["invocations"])
        assert context.body["invocations"] == [1, 2, 3]