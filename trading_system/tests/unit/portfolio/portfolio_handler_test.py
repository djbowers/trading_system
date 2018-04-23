import unittest
from trading_system.portfolio import PortfolioHandler


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.portfolio_handler = PortfolioHandler()

    def test_for_error_on_update_on_signal(self):
        self.assertRaises(NotImplementedError, self.portfolio_handler.generate_order_from_signal, None)

    def test_for_error_on_update_on_fill(self):
        self.assertRaises(NotImplementedError, self.portfolio_handler.update_portfolio_on_fill, None)

    def test_for_error_on_update_on_market(self):
        self.assertRaises(NotImplementedError, self.portfolio_handler.update_portfolio_on_market, None)
