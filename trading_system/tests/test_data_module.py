import unittest

from .. import data_handlers
from ..event_queue import EventQueue
from . import TEST_DATA_DIR
from .data_validation import SYMBOL_LIST, SAMPLE1_PARSED
from ..events import MarketEvent
import queue


class TestHistoricCSVDataHandler(unittest.TestCase):

    def setUp(self):
        self.data_handler = data_handlers.create('historic_csv', EventQueue(), TEST_DATA_DIR, SYMBOL_LIST)
        self.data_handler.update_bars()

    def test_unavailable_symbol(self):
        self.assertRaises(KeyError, self.data_handler.get_latest_bars, 'invalid')

    def test_market_event_added_to_event_queue(self):
        try:
            event = self.data_handler.event_queue.get_nowait()
        except queue.Empty:
            event = None
        self.assertIsInstance(event, MarketEvent,
                              "The next event in the queue was not a market event.")

    def test_get_first_bar(self):
        latest_bars = self.data_handler.get_latest_bars('sample1', N=1)[0]

        first_bar = next(latest_bars)
        print(first_bar)
        second_bar = next(latest_bars)
        print(second_bar)

        self.assertEqual(SAMPLE1_PARSED[0], first_bar,
                         "First bar does not match values from CSV file.")

    def test_get_second_bar(self):
        latest_bars = self.data_handler.get_latest_bars(self.data_handler.symbol_list[0], N=2)[0]
        next(latest_bars)
        second_bar = next(latest_bars)

        self.assertEqual(SAMPLE1_PARSED[1], second_bar,
                         "Second bar does not match values from CSV file.")


if __name__ == '__main__':
    unittest.main()

