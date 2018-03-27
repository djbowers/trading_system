from enum import Enum

from .naive import NaivePortfolio


def create_portfolio(portfolio_type, *args, **kwargs):
    if portfolio_type == PortfolioType.NAIVE:
        return NaivePortfolio(*args, **kwargs)


class PortfolioType(Enum):
    NAIVE = 1
