from enum import Enum

from .backtesting import BacktestingSession


def create_session(trading_type, *args, **kwargs):
    if trading_type == SessionType.BACKTESTING:
        return BacktestingSession(*args, **kwargs)
    elif trading_type == SessionType.LIVE:
        pass
    else:
        raise ImportError('{} is not a valid session type.'.format(trading_type))


class SessionType(Enum):
    BACKTESTING: 1
    LIVE: 2
