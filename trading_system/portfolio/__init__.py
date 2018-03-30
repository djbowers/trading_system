from .base import BasePortfolio
from .naive import NaivePortfolio
from .type import PortfolioType


def create_portfolio(portfolio_type, *args, **kwargs):
    if portfolio_type == PortfolioType.NAIVE:
        return NaivePortfolio(*args, **kwargs)
