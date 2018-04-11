class Report:
    """
    The Report data structure represents the results of the trading session
    as a report.
    """

    def __init__(self, equity_curve, summary_stats):
        self.equity_curve = equity_curve
        self.total_return = summary_stats['total_return']
        self.sharpe_ratio = summary_stats['sharpe_ratio']
        self.max_drawdown = summary_stats['max_drawdown']
        self.drawdown_duration = summary_stats['drawdown_duration']

    def __repr__(self):
        return ("=====================================\n" +
                "======== Backtesting Results ========\n\n" +
                "Total Return: {:0.2f}%\n".format((self.total_return - 1.0) * 100.0) +
                "Sharpe Ratio: {:0.2f}\n".format(self.sharpe_ratio) +
                "Max Drawdown: {:0.2f}%\n".format(self.max_drawdown * 100.0) +
                "Drawdown Duration: {}\n\n".format(self.drawdown_duration) +
                "=====================================")
