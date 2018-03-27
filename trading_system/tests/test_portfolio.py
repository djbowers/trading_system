import unittest

from .. import portfolios
from ..portfolios import PortfolioType
from ..event_queue import EventQueue
from ..price_handler.base import BasePriceHandler
from datetime import datetime
from . import SYMBOLS


class PriceHandlerMock(BasePriceHandler):
    def __init__(self):
        self.symbols = SYMBOLS

    def get_latest_bars(self, symbol, num_bars=1):
        return None

    def update_bars(self):
        pass


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        self.start_date = datetime(2018, 3, 25, 23, 3, 4, 18896)
        self.portfolio = portfolios.create(PortfolioType.NAIVE, PriceHandlerMock(), EventQueue(), datetime.now())

    def test_all_positions_start_date(self):
        portfolio_start_date = self.portfolio.all_holdings['datetime']
        self.assertEqual(portfolio_start_date, self.start_date,
                         "The start date of Portfolio.all_holdings should match the start")

