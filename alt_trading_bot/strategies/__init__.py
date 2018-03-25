from .buy_and_hold_strategy import BuyAndHoldStrategy


def create(strategy_type, *args, **kwargs):
    if strategy_type == 'buy_and_hold':
        return BuyAndHoldStrategy(*args, **kwargs)
