import unittest
from queue import Empty as EmptyQueue

from config import TestingConfig
from trading_system.data import GDAXCSVDataHandler
from trading_system.errors import SymbolError
from trading_system.events import MarketEvent, EventQueue


class TestGDAXCSVPriceHandler(unittest.TestCase):
    """
    Test the initialisation of a PriceHandler object with a small list of symbols.
    """

    def setUp(self):
        self.price_handler = GDAXCSVDataHandler(EventQueue(),
                                                TestingConfig.DATA_DIR,
                                                TestingConfig.SYMBOLS)

    def test_get_latest_bars_raises_symbol_error_when_passed_invalid_symbol(self):
        self.assertRaises(SymbolError, self.price_handler.get_latest_bars, 'XRP',
                          "XRP is not a valid symbol.")

    def test_update_bars_adds_market_event_to_event_queue(self):
        self.price_handler.update_bars()
        event_queue = self.price_handler.events
        try:
            event = event_queue.get_next_event()
        except EmptyQueue:
            event = None

        self.assertIsInstance(event, MarketEvent,
                              "The next event in the queue was not a market event.")

    def test_get_latest_bars_returns_first_bar_correctly(self):
        self.price_handler.update_bars()

        latest_bars = self.price_handler.get_latest_bars('BTC')
        latest_bar_gen = latest_bars.pop()
        first_bar = next(latest_bar_gen)
        first_bar_time = first_bar[1]

        self.assertEqual('2018-03-01 00:00:00', first_bar_time,
                         "First bar does not match values from CSV file.")

    def test_get_latest_bars_returns_fifth_bar_correctly(self):
        self.price_handler.update_bars()

        latest_bars = self.price_handler.get_latest_bars('BTC')
        latest_bar_gen = latest_bars.pop()

        num_iters = 5
        for _ in range(num_iters-1):
            next(latest_bar_gen)
        fifth_bar = next(latest_bar_gen)
        fifth_bar_time = fifth_bar[1]

        self.assertEqual('2018-03-01 04:00:00', fifth_bar_time,
                         "Fifth bar does not match values from CSV file.")


if __name__ == '__main__':
    unittest.main()

