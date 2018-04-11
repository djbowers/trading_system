import numpy as np
import pandas as pd


def create_sharpe_returns(returns, periods=365):
    """
    Create the Sharpe ratio for the strategy, based on a benchmark of zero
    (i.e. no risk-free rate information).

    Args:
        returns: A pandas Series representing period percentage returns
        periods: Daily (365), Hourly (365*24), Minutely (365*24*60) etc.
    """
    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_drawdowns(equity_curve):
    """
    Calculate the largest peak-to-trough drawdown of the PnL curve
    as well as the duration of the drawdown. Requires that the
    pnl_returns is a pandas Series.

    Args:
        equity_curve: A pandas Series representing period percentage returns

    Returns:
        drawdown, duration: Highest peak-to-trough drawdown and duration
    """

    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    # Then create the drawdown and duration series
    hwm = [0]
    eq_idx = equity_curve.index
    drawdown = pd.Series(index=eq_idx)
    duration = pd.Series(index=eq_idx)

    # Loop over the index range
    for t in range(1, len(eq_idx)):
        cur_hwm = max(hwm[t-1], equity_curve[t])
        hwm.append(cur_hwm)
        drawdown[t] = hwm[t] - equity_curve[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t-1] + 1
    return drawdown.max(), duration.max()
