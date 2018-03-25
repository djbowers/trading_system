from .naive_portfolio import NaivePortfolio


def create(portfolio_type, *args, **kwargs):
    if portfolio_type == 'naive':
        return NaivePortfolio(*args, **kwargs)
