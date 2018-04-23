import unittest
from trading_system.portfolio import NaivePortfolio
from config import TestingConfig


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        self.symbols = TestingConfig.SYMBOLS
        self.start_date = '2018-02-28 00:00:00'
        self.portfolio = NaivePortfolio(self.symbols, self.start_date)

    def test_init_sets_current_positions(self):
        self.assertEqual(self.portfolio.current_positions,
                         {'BTC': 0, 'ETH': 0, 'LTC': 0})

    def test_init_sets_all_positions(self):
        self.assertEqual(self.portfolio.all_positions,
                         [{'BTC': 0, 'ETH': 0, 'LTC': 0, 'datetime': self.start_date}])

    def test_init_sets_current_holdings(self):
        self.assertEqual(self.portfolio.current_holdings,
                         {'BTC': 0.0, 'ETH': 0.0, 'LTC': 0.0, 'cash': 100000.0,
                          'fees': 0.0, 'total': 100000.0})

    def test_init_sets_all_holdings(self):
        self.assertEqual(self.portfolio.all_holdings,
                         [{'BTC': 0.0, 'ETH': 0.0, 'LTC': 0.0, 'datetime': self.start_date,
                           'cash': 100000.0, 'fees': 0.0, 'total': 100000.0}])
