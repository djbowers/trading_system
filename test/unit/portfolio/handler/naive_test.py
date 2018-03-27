import unittest
from datetime import datetime

from trading_system import portfolio
from trading_system.event_queue import EventQueue
from trading_system.price.handler.base import BasePriceHandler


class PriceHandlerMock(BasePriceHandler):
    def __init__(self):
        self.symbols = ['BTC', 'ETH', 'LTC']  # todo: replace with config.SYMBOLS

    def get_latest_bars(self, symbol, num_bars=1):
        return None

    def update_bars(self):
        pass


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime(2018, 3, 25, 23, 3, 4, 18896)
        self.portfolio = portfolio.create_portfolio(portfolio.PortfolioType.NAIVE, PriceHandlerMock(), EventQueue(), datetime.now())

    def test_all_positions_start_date(self):
        portfolio_start_date = self.portfolio.all_holdings['datetime']
        self.assertEqual(portfolio_start_date, self.start_date,
                         "The start date of Portfolio.all_holdings should match the start")

