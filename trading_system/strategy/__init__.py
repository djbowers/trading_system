from enum import Enum

from .buy_and_hold import BuyAndHoldStrategy


def create(strategy_type, *args, **kwargs):
    if strategy_type == StrategyType.BUY_AND_HOLD:
        return BuyAndHoldStrategy(*args, **kwargs)


class StrategyType(Enum):
    BUY_AND_HOLD: 1
