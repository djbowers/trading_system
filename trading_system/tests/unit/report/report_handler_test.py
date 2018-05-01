import unittest

from trading_system.portfolio import Portfolio
from trading_system.report import ReportHandler


class TestReportHandler(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio()
        self.report_handler = ReportHandler(self.portfolio)
        self.report = self.report_handler.generate_report()

    # def test_for_report_equity(self):
    #     self.assertEqual(self.report.equity_curve['equity'][-1], 1.02)
    #
    # def test_for_total_return(self):
    #     self.assertEqual(self.report.total_return, 1.02)
    #
    # def test_for_sharpe_ratio(self):
    #     self.assertAlmostEqual(self.report.sharpe_ratio, 7.55, places=2)
    #
    # def test_for_max_drawdown(self):
    #     self.assertAlmostEqual(self.report.max_drawdown, 0.01, places=2)
    #
    # def test_for_drawdown_duration(self):
    #     self.assertEqual(self.report.drawdown_duration, 1)
