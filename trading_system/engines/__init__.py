from .backtesting import BacktestingEngine
from .engine import Engine


def get(engine_type, *args, **kwargs):
    if engine_type == EngineType.BACKTESTING:
        return BacktestingEngine(*args, **kwargs)
    elif engine_type == EngineType.LIVE:
        pass
    else:
        raise ImportError('{} is not a valid session type.'.format(engine_type))


class EngineType:
    BACKTESTING = 1
    LIVE = 2
