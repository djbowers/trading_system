import unittest

from config import TestingConfig
from trading_system.data import GDAXCSVDataHandler
from trading_system.errors import SymbolError
from trading_system.event import EventQueue, EventType


class TestGDAXCSVDataHandler(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.symbols = TestingConfig.SYMBOLS
        self.csv_dir = TestingConfig.DATA_DIR
        self.data_handler = GDAXCSVDataHandler(self.events, self.symbols, self.csv_dir)

    def test_for_symbol_error_when_get_latest_bars_given_invalid_symbol(self):
        self.assertRaises(SymbolError, self.data_handler.get_latest_bars, 'INVALID')

    def test_for_attribute_error_when_initialized_with_empty_symbols_param(self):
        symbols = []
        self.assertRaises(AttributeError, GDAXCSVDataHandler, EventQueue(), symbols, self.csv_dir)

    def test_for_market_event_after_update_bars(self):
        self.data_handler.update_bars()
        event = self.events.get_next_event()
        self.assertEqual(event.type, EventType.MARKET)

    def test_that_get_latest_bars_returns_1st_bar(self):
        self.data_handler.update_bars()
        bars = self.data_handler.get_latest_bars('BTC')
        self.assertEqual('2018-03-01 00:00:00', bars[0].time)

    def test_that_get_latest_bars_returns_5th_bar(self):
        for _ in range(5):
            self.data_handler.update_bars()
        bars = self.data_handler.get_latest_bars('BTC')
        self.assertEqual('2018-03-01 04:00:00', bars[0].time)

    def test_that_get_latest_bars_returns_3_bars(self):
        for _ in range(3):
            self.data_handler.update_bars()
        bars = self.data_handler.get_latest_bars('BTC', num_bars=3)
        self.assertEqual('2018-03-01 02:00:00', bars[2].time)

    def test_that_update_bars_raises_stop_iteration(self):
        for _ in range(25):
            self.data_handler.update_bars()
        self.assertEqual(self.data_handler.continue_backtest, False)
