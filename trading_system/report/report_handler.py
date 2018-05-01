import pandas as pd

from trading_system.portfolio import Portfolio
from .performance import create_drawdowns, create_sharpe_returns
from .report import Report


class ReportHandler:
    """
    The ReportHandler class generates reports based on the holdings
    data in the Portfolio structure.
    """

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def generate_report(self) -> Report:
        """
        Generate a new report from the current portfolio data.
        """
        # equity_curve = self._generate_equity_curve()
        # summary_stats = self._generate_summary_stats(equity_curve)
        # return Report(equity_curve, summary_stats)
        pass
    #
    # def _generate_equity_curve(self):
    #     """
    #     Creates a pandas DataFrame from the all_holdings list of dictionaries.
    #     """
    #     curve = pd.DataFrame(self.portfolio.all_holdings)
    #     curve.set_index('datetime', inplace=True)
    #     curve['returns'] = curve['total'].pct_change()
    #     curve['equity'] = (1.0+curve['returns']).cumprod()
    #     return curve
    #
    # @staticmethod
    # def _generate_summary_stats(equity_curve):
    #     """
    #     Creates a list of summary statistics for the portfolio such as
    #     Sharpe Ratio and drawdown information.
    #     """
    #     total_return = equity_curve['equity'][-1]
    #     returns = equity_curve['returns']
    #     pnl = equity_curve['equity']
    #
    #     sharpe_ratio = create_sharpe_returns(returns)
    #     max_drawdown, drawdown_duration = create_drawdowns(pnl)
    #
    #     return {'total_return': total_return,
    #             'sharpe_ratio': sharpe_ratio,
    #             'max_drawdown': max_drawdown,
    #             'drawdown_duration': drawdown_duration}
