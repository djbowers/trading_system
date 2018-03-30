import unittest
from datetime import datetime

from trading_system import portfolio
from trading_system.event_queue import EventQueue
from trading_system.price_handler.base import BasePriceHandler
from trading_system.config import TestingConfig


class PriceHandlerMock(BasePriceHandler):
    def __init__(self):
        config = TestingConfig()
        self.symbols = config.SYMBOLS

    def get_latest_bars(self, symbol, num_bars=1):
        return None

    def update_bars(self):
        pass


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime(2018, 3, 25, 23, 3, 4, 18896)
        self.portfolio = portfolio.create_portfolio(portfolio.PortfolioType.NAIVE, PriceHandlerMock(), EventQueue(), datetime.now())

