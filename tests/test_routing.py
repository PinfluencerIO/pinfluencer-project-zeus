from unittest import TestCase
from unittest.mock import MagicMock, call

from src.web import PinfluencerContext
from src.web.routing import MiddlewarePipeline


class TestMiddlewarePipeline(TestCase):

    def setUp(self) -> None:
        self.__sut = MiddlewarePipeline()

    def test_execute(self):

        # arrange
        middlware_spy = MagicMock()
        middlware = [MagicMock(side_effect=lambda: middlware_spy(1)),
                     MagicMock(side_effect=lambda: middlware_spy(2)),
                     MagicMock(side_effect=lambda: middlware_spy(3)),
                     MagicMock(side_effect=lambda: middlware_spy(4)),
                     MagicMock(side_effect=lambda: middlware_spy(5))]

        # act
        self.__sut.execute_middleware(context=PinfluencerContext(),
                                      middleware=middlware)

        # assert
        middlware_spy.assert_has_calls(calls=[
            call(1),
            call(2),
            call(3),
            call(4),
            call(5)
        ], any_order=False)