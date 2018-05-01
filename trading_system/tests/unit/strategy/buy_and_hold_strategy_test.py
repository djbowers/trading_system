import unittest

from config import TestingConfig
from trading_system.event import MarketEvent, EventQueue, EventType
from trading_system.strategy import BuyAndHoldStrategy
from trading_system.data import PriceBar


class TestBuyAndHoldStrategyTest(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.symbols = TestingConfig.SYMBOLS
        self.strategy = BuyAndHoldStrategy(self.events, self.symbols)

    def test_that_calculate_signals_adds_signal_event_to_event_queue(self):
        symbol = 'BTC'
        bar = PriceBar('2018-02-28 12:00:00', 0, 0, 0, 0, 0, symbol)
        market_event = MarketEvent({symbol: [bar]})
        self.strategy.calculate_signals(market_event)
        event = self.events.get_next_event()
        self.assertEqual(event.type, EventType.SIGNAL)
