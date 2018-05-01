import unittest
from trading_system.portfolio import Portfolio
from trading_system.event import FillEvent, MarketEvent
from trading_system.data import PriceBar
from decimal import Decimal


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        fill = FillEvent('0:00', 'BTC', 10, "BUY", 100, 'GDAX', fee=5.0)
        self.portfolio = Portfolio(cash=10000.0)
        self.portfolio.add_new_fill(fill)

    def test_cash(self):
        self.assertEqual(self.portfolio.cash, Decimal("8995"))

    def test_market_value(self):
        self.assertEqual(self.portfolio.market_value, Decimal("1000"))

    def test_equity(self):
        self.assertEqual(self.portfolio.equity, Decimal("9995"))

    def test_fees(self):
        self.assertEqual(self.portfolio.fees, Decimal("5"))

    def test_cost_basis(self):
        self.assertEqual(self.portfolio.cost_basis, Decimal("1005"))

    def test_realized_pnl(self):
        self.assertEqual(self.portfolio.realized_pnl, Decimal("0"))

    def test_unrealized_pnl(self):
        symbol = 'BTC'
        bar = PriceBar('1:00', 100, 95, 115, 105, 100, symbol)
        market = MarketEvent({symbol: [bar]})
        self.portfolio.update_market_value(market)
        self.assertEqual(self.portfolio.unrealized_pnl, Decimal("50"))


class TestPortfolioWithTwoFills(unittest.TestCase):

    def setUp(self):
        first_fill = FillEvent('0:00', 'BTC', 10, "BUY", 100, 'GDAX', fee=5.0)
        second_fill = FillEvent('1:00', 'BTC', 15, "BUY", 125, 'GDAX', fee=10.0)
        self.portfolio = Portfolio(cash=10000.0)
        self.portfolio.add_new_fill(first_fill)
        self.portfolio.add_new_fill(second_fill)

    def test_cash(self):
        self.assertEqual(self.portfolio.cash, Decimal("7110"))

    def test_market_value(self):
        self.assertEqual(self.portfolio.market_value, Decimal("3125"))

    def test_equity(self):
        self.assertEqual(self.portfolio.equity, Decimal("10235"))

    def test_fees(self):
        self.assertEqual(self.portfolio.fees, Decimal("15"))

    def test_cost_basis(self):
        self.assertEqual(self.portfolio.cost_basis, Decimal("2890"))

    def test_realized_pnl(self):
        self.assertEqual(self.portfolio.realized_pnl, Decimal("0"))

    def test_unrealized_pnl(self):
        self.assertEqual(self.portfolio.unrealized_pnl, Decimal("250"))

    def test_unrealized_pnl_after_market_update(self):
        symbol = 'BTC'
        bar = PriceBar('2:00', 100, 95, 115, 150, 100, symbol)
        market = MarketEvent({symbol: [bar]})
        self.portfolio.update_market_value(market)
        self.assertEqual(self.portfolio.unrealized_pnl, Decimal("875"))

    def test_total_pnl(self):
        self.assertEqual(self.portfolio.total_pnl, Decimal("250"))
