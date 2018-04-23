import unittest

from config import TestingConfig
from trading_system.portfolio import NaivePortfolio
from trading_system.report import ReportHandler


class TestReportHandler(unittest.TestCase):

    def setUp(self):
        self.symbols = TestingConfig.SYMBOLS
        self.start_date = '2018-02-28 00:00:00'
        self.portfolio = NaivePortfolio(self.symbols, self.start_date)
        self.portfolio.all_holdings = [
            {'datetime': '0', 'cash': 100000.0, 'BTC':     0.0, 'total': 100000.0},
            {'datetime': '1', 'cash':  90000.0, 'BTC': 10000.0, 'total': 100000.0},
            {'datetime': '2', 'cash':  90000.0, 'BTC':  9000.0, 'total':  99000.0},
            {'datetime': '3', 'cash':  90000.0, 'BTC': 12000.0, 'total': 102000.0},
        ]
        self.report_handler = ReportHandler(self.portfolio)
        self.report = self.report_handler.generate_report()

    def test_for_report_equity(self):
        self.assertEqual(self.report.equity_curve['equity'][-1], 1.02)

    def test_for_total_return(self):
        self.assertEqual(self.report.total_return, 1.02)

    def test_for_sharpe_ratio(self):
        self.assertAlmostEqual(self.report.sharpe_ratio, 7.55, places=2)

    def test_for_max_drawdown(self):
        self.assertAlmostEqual(self.report.max_drawdown, 0.01, places=2)

    def test_for_drawdown_duration(self):
        self.assertEqual(self.report.drawdown_duration, 1)
