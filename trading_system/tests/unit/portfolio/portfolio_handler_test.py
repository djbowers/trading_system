import unittest
from decimal import Decimal

from trading_system.event import EventQueue, SignalEvent, EventType, FillEvent, MarketEvent
from trading_system.portfolio import PortfolioHandler, Portfolio, PositionSizerMock, RiskManagerMock
from trading_system.data import PriceBar


class TestPortfolioHandler(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.portfolio = Portfolio()
        position_sizer = PositionSizerMock()
        risk_manager = RiskManagerMock()
        self.portfolio_handler = PortfolioHandler(self.events, self.portfolio, position_sizer, risk_manager)

        self.fill = FillEvent(
            timeindex='0:00', symbol='BTC', quantity=10, price=100,
            direction='BUY', exchange='GDAX'
        )

    def test_update_on_signal_adds_order_event(self):
        signal_event = SignalEvent('BTC', '0:00', 'LONG')
        self.portfolio_handler.generate_order_from_signal(signal_event)
        order_event = self.events.get_next_event()
        self.assertEqual(order_event.type, EventType.ORDER)

    def test_update_on_fill_adds_position(self):
        self.assertDictEqual(self.portfolio.positions, {})
        self.portfolio_handler.update_portfolio_on_fill(self.fill)
        self.assertListEqual(self.portfolio.positions['BTC'].fills, [self.fill])

    def test_update_on_market(self):
        self.portfolio_handler.update_portfolio_on_fill(self.fill)
        symbol = 'BTC'
        bar = PriceBar('1:00', 100, 95, 110, 105, 100, symbol)
        market = MarketEvent({symbol: [bar]})
        self.portfolio_handler.update_portfolio_on_market(market)
        self.assertEqual(self.portfolio.market_value, Decimal("1050"))
