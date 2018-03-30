from .backtesting import BacktestingSession
from .base import BaseTradingSession
from .type import SessionType


def create_session(trading_type, *args, **kwargs):
    if trading_type == SessionType.BACKTESTING:
        return BacktestingSession(*args, **kwargs)
    elif trading_type == SessionType.LIVE:
        pass
    else:
        raise ImportError('{} is not a valid session type.'.format(trading_type))
