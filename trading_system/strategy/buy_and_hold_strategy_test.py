import unittest
from trading_system.strategy import BuyAndHoldStrategy
from unittest.mock import Mock
from trading_system.events import MarketEvent, SignalEvent, EventQueue
from config import TestingConfig


class TestBuyAndHoldStrategyTest(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.data_handler = Mock(symbols=TestingConfig.SYMBOLS)
        # bar = [symbol, formatted_time, low_of_bar, high_of_bar, open_of_bar, close_of_bar, volume_of_bar]
        # self.data_handler.get_latest_bars.return_value = bar
        self.strategy = BuyAndHoldStrategy(self.data_handler, self.events)

    # def test_calculate_signals_adds_signal_event_to_event_queue(self):
    #     self.strategy.calculate_signals(MarketEvent())
    #     event = self.events.maybe_get_next_event()
    #     self.assertIsInstance(event, SignalEvent,
    #                           'The strategy did not correctly add a signal event to the event queue')


if __name__ == '__main__':
    unittest.main()
