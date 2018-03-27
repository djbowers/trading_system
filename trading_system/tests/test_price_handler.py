import unittest
from queue import Empty as EmptyQueue

from . import TEST_DATA_DIR, SYMBOLS
from .. import price_handler
from ..event_queue import EventQueue
from ..events import MarketEvent
from ..price_handler import DataType, SymbolError


class TestGdaxCsvPriceHandler(unittest.TestCase):
    """
    Test the initialisation of a PriceHandler object with a small list of symbols.
    """

    def setUp(self):
        """
        Set up the PriceHandler object.
        """
        self.price_handler = price_handler.create(DataType.GDAX_CSV, EventQueue(), TEST_DATA_DIR, SYMBOLS)

    def test_get_latest_bars_with_invalid_symbol(self):
        """Test that a Symbol Error is raised when get_latest_bars() is passed an invalid symbol."""
        self.assertRaises(SymbolError, self.price_handler.get_latest_bars, 'XRP',
                          "XRP is not a valid symbol.")

    def test_update_bars_adds_market_event(self):
        """Test that a MarketEvent is added to the EventQueue after update_bars()."""
        self.price_handler.update_bars()
        event_queue = self.price_handler.event_queue
        try:
            event = event_queue.get_next_event()
        except EmptyQueue:
            event = None

        self.assertIsInstance(event, MarketEvent,
                              "The next event in the queue was not a market event.")

    def test_get_first_bar_time_btc(self):
        """Test that we can get the first bar from a CSV file."""
        self.price_handler.update_bars()

        latest_bars = self.price_handler.get_latest_bars('BTC')
        latest_bar_gen = latest_bars.pop()
        first_bar = next(latest_bar_gen)
        first_bar_time = first_bar[1]

        self.assertEqual('2018-03-01 00:00:00', first_bar_time,
                         "First bar does not match values from CSV file.")

    def test_get_fifth_bar_time_btc(self):
        """Test that we can get the fifth bar from a CSV file."""
        self.price_handler.update_bars()

        latest_bars = self.price_handler.get_latest_bars('BTC')
        latest_bar_gen = latest_bars.pop()

        num_iters = 5
        for _ in range(num_iters-1):
            next(latest_bar_gen)
        fifth_bar = next(latest_bar_gen)
        fifth_bar_time = fifth_bar[1]

        self.assertEqual('2018-03-01 04:00:00', fifth_bar_time,
                         "First bar does not match values from CSV file.")


if __name__ == '__main__':
    unittest.main()

