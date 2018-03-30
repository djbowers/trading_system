import unittest
from datetime import datetime

from trading_system.portfolio_handler import NaivePortfolioHandler
from trading_system.events import EventQueue
from unittest.mock import Mock


class TestNaivePortfolio(unittest.TestCase):

    def setUp(self):
        start_date = datetime(2018, 3, 25, 23, 3, 4, 18896)
        events = EventQueue()
        data_handler = Mock()
        self.portfolio = NaivePortfolioHandler(data_handler, events, start_date)

