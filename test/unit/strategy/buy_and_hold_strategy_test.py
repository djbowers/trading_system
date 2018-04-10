import unittest

from config import TestingConfig
from trading_system.event import MarketEvent, EventQueue
from trading_system.strategy import BuyAndHoldStrategy


class TestBuyAndHoldStrategyTest(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.symbols = TestingConfig.SYMBOLS
        # bar = [symbol, formatted_time, low_of_bar, high_of_bar, open_of_bar, close_of_bar, volume_of_bar]
        # self.data_handler.get_latest_bars.return_value = bar
        self.strategy = BuyAndHoldStrategy(self.events, self.symbols)

    # def test_calculate_signals_adds_signal_event_to_event_queue(self):
    #     self.strategy.calculate_signals(MarketEvent())
    #     event = self.events.maybe_get_next_event()
    #     self.assertEqual(event.type, 'SIGNAL')


if __name__ == '__main__':
    unittest.main()
