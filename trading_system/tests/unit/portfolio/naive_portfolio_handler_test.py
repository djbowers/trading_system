import unittest

import pandas as pd

from config import TestingConfig
from trading_system.data import PriceBar
from trading_system.event import EventQueue, SignalEvent, FillEvent, MarketEvent, EventType
from trading_system.portfolio import NaivePortfolioHandler, Portfolio


class TestNaivePortfolioHandler(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.symbols = TestingConfig.SYMBOLS
        self.start_date = '2018-02-28 00:00:00'
        self.portfolio = Portfolio(self.symbols, self.start_date)
        self.portfolio_handler = NaivePortfolioHandler(self.events, self.portfolio)

    def test_that_update_on_signal_adds_order_event(self):
        signal_event = SignalEvent('BTC', '2018-02-28 12:00:00', 'LONG')
        self.portfolio_handler.update_on_signal(signal_event)
        order_event = self.events.get_next_event()
        self.assertEqual(order_event.type, EventType.ORDER)

    def test_that_update_on_fill_sets_current_positions(self):
        fill_event = FillEvent('2018-02-28 12:00:00', 'BTC', 10, 'BUY', 1000, 'GDAX')
        self.portfolio_handler.update_on_fill(fill_event)
        self.assertEqual(self.portfolio_handler.portfolio.current_positions,
                         {'BTC': 10, 'ETH': 0, 'LTC': 0})

    def test_that_update_on_fill_sets_current_holdings(self):
        fill_event = FillEvent('2018-02-28 12:00:00', 'BTC', 10, 'BUY', 1000, 'GDAX')
        self.portfolio_handler.update_on_fill(fill_event)
        self.assertEqual(self.portfolio_handler.portfolio.current_holdings,
                         {'BTC': 10000.0, 'ETH': 0.0, 'LTC': 0.0, 'cash': 90000.0,
                          'fees': 0.0, 'total': 90000.0})

    def test_that_update_on_market_adds_to_all_positions(self):
        symbol = 'BTC'
        bar = PriceBar('2018-02-28 12:00:00', 0, 0, 0, 0, 0, symbol)
        market_event = MarketEvent({symbol: [bar]})
        self.portfolio_handler.update_on_market(market_event)
        self.assertEqual(len(self.portfolio_handler.portfolio.all_positions), 2)

    def test_that_update_on_market_adds_to_all_holdings(self):
        symbol = 'BTC'
        bar = PriceBar('2018-02-28 12:00:00', 0, 0, 0, 0, 0, symbol)
        market_event = MarketEvent({symbol: [bar]})
        self.portfolio_handler.update_on_market(market_event)
        self.assertEqual(len(self.portfolio_handler.portfolio.all_holdings), 2)

    def test_for_equity_after_create_equity_curve(self):
        self.portfolio.all_holdings = [
            {'datetime': '0', 'cash': 100000.0, 'BTC':     0.0, 'total': 100000.0},
            {'datetime': '1', 'cash':  90000.0, 'BTC': 10000.0, 'total': 100000.0},
            {'datetime': '2', 'cash':  90000.0, 'BTC':  9000.0, 'total':  99000.0},
            {'datetime': '3', 'cash':  90000.0, 'BTC': 12000.0, 'total': 102000.0},
        ]
        self.portfolio_handler.create_equity_curve()
        self.assertEqual(self.portfolio.equity_curve['equity'][-1], 1.02)


class TestNaivePortfolioHandlerPerformance(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.symbols = TestingConfig.SYMBOLS
        self.start_date = '0'
        self.portfolio = Portfolio(self.symbols, self.start_date)
        self.portfolio_handler = NaivePortfolioHandler(self.events, self.portfolio)
        data = [
            {'datetime': '0', 'cash': 100000.0, 'BTC':     0.0, 'total': 100000.0, 'returns': None,   'equity': None},
            {'datetime': '1', 'cash':  90000.0, 'BTC': 10000.0, 'total': 100000.0, 'returns': 0.0,    'equity': 1.0},
            {'datetime': '2', 'cash':  90000.0, 'BTC':  9000.0, 'total':  99000.0, 'returns': -0.01,  'equity': 0.99},
            {'datetime': '3', 'cash':  90000.0, 'BTC': 12000.0, 'total': 102000.0, 'returns': 0.0303, 'equity': 1.02},
        ]
        self.portfolio.equity_curve = pd.DataFrame(data)
        self.portfolio.equity_curve.set_index('datetime', inplace=True)

    def test_for_total_return_from_output_summary_stats(self):
        stats = self.portfolio_handler.output_summary_stats()
        self.assertEqual(stats[0], ('Total Return', '2.00%'))

    def test_for_sharpe_ratio_from_output_summary_stats(self):
        stats = self.portfolio_handler.output_summary_stats()
        self.assertEqual(stats[1], ('Sharpe Ratio', '7.55'))

    def test_for_max_drawdown_from_output_summary_stats(self):
        stats = self.portfolio_handler.output_summary_stats()
        self.assertEqual(stats[2], ('Max Drawdown', '1.00%'))

    def test_for_drawdown_duration_from_output_summary_stats(self):
        stats = self.portfolio_handler.output_summary_stats()
        self.assertEqual(stats[3], ('Drawdown Duration', '1'))
