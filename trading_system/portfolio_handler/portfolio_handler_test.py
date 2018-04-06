import unittest

from trading_system.data import DataHandler, GDAXCSVDataHandler
from trading_system.events import EventQueue, SignalEvent, OrderEvent, FillEvent, MarketEvent
from trading_system.portfolio_handler import NaivePortfolioHandler
from config import TestingConfig


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        self.start_date = '2018-02-28 00:00:00'
        self.fill_date = '2018-02-28 12:00:00'
        self.fill_event = FillEvent(self.fill_date, 'BTC', 10, 'BUY', 1000, 'GDAX')
        self.events = EventQueue()
        data_handler = GDAXCSVDataHandler(self.events, TestingConfig.DATA_DIR, TestingConfig.SYMBOLS)  # temp
        self.portfolio_handler = NaivePortfolioHandler(data_handler, self.events, self.start_date)
        self.portfolio_handler.data_handler.update_bars()
        self.events.maybe_get_next_event()  # remove the MarketEvent from update_bars()

    def test_init_sets_current_positions(self):
        self.assertEqual(self.portfolio_handler.current_positions,
                         {'BTC': 0, 'ETH': 0, 'LTC': 0})

    def test_init_sets_all_positions(self):
        self.assertEqual(self.portfolio_handler.all_positions,
                         [{'BTC': 0, 'ETH': 0, 'LTC': 0, 'datetime': self.start_date}])

    def test_init_sets_current_holdings(self):
        self.assertEqual(self.portfolio_handler.current_holdings,
                         {'BTC': 0.0, 'ETH': 0.0, 'LTC': 0.0, 'cash': 100000.0,
                          'fees': 0.0, 'total': 100000.0})

    def test_init_sets_all_holdings(self):
        self.assertEqual(self.portfolio_handler.all_holdings,
                         [{'BTC': 0.0, 'ETH': 0.0, 'LTC': 0.0, 'datetime': self.start_date,
                           'cash': 100000.0, 'fees': 0.0, 'total': 100000.0}])

    def test_update_signal_adds_order_event(self):
        signal_event = SignalEvent('BTC', self.fill_date, 'LONG')
        self.portfolio_handler.update_on_signal(signal_event)
        order_event = self.events.maybe_get_next_event()
        self.assertIsInstance(order_event, OrderEvent)

    def test_update_fill_sets_current_positions(self):
        self.portfolio_handler.update_on_fill(self.fill_event)
        self.assertEqual(self.portfolio_handler.current_positions,
                         {'BTC': 10, 'ETH': 0, 'LTC': 0})

    def test_update_fill_sets_current_holdings(self):
        self.portfolio_handler.update_on_fill(self.fill_event)
        self.assertEqual(self.portfolio_handler.current_holdings,
                         {'BTC': 10000.0, 'ETH': 0.0, 'LTC': 0.0, 'cash': 90000.0,
                          'fees': 0.0, 'total': 90000.0})

    def test_update_portfolio_adds_to_all_positions(self):
        self.portfolio_handler.update_portfolio(MarketEvent())
        self.assertEqual(len(self.portfolio_handler.all_positions), 2)

    def test_update_portfolio_adds_to_all_holdings(self):
        self.portfolio_handler.update_portfolio(MarketEvent())
        self.assertEqual(len(self.portfolio_handler.all_holdings), 2)


class DataHandlerMock(DataHandler):

    def __init__(self):
        self.symbols = TestingConfig.SYMBOLS

    def get_latest_bars(self, symbol, num_bars=1):
        pass

    def update_bars(self):
        pass


if __name__ == '__main__':
    unittest.main()

