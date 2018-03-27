from .naive_portfolio import NaivePortfolio

from enum import Enum

PortfolioType = Enum('PortfolioType', 'NAIVE')


def create(portfolio_type, *args, **kwargs):
    if portfolio_type == PortfolioType.NAIVE:
        return NaivePortfolio(*args, **kwargs)
