from trading_system.performance import create_drawdowns, create_sharpe_returns
import unittest
import pandas as pd


class TestPerformance(unittest.TestCase):

    def test_create_sharpe_returns(self):
        returns = pd.Series()
        sharpe_ratio = create_sharpe_returns(returns)

    # def test_create_drawdowns(self):
    #     equity_curve = []
    #     drawdowns = create_drawdowns(equity_curve)
