from abc import ABCMeta


class BaseTradingSession:
    """
    The trading session initializes the type of trading that will
    be performed, whether it be backtesting or live trading.
    """

    __metaclass__ = ABCMeta
