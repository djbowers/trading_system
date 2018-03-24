from abc import ABC, abstractmethod

from . import NaivePortfolio


class Portfolio(ABC):
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e. secondly, minutely, 5-min, 30-min, 60 min, or EOD.
    """

    @staticmethod
    def create_new_portfolio(portfolio_type, **kwargs):
        """
        Factory method for creating new Portfolios.
        """
        if portfolio_type == 'naive':
            if 'initial_capital' in kwargs.keys():
                return NaivePortfolio(kwargs['data_handler'], kwargs['event_queue'], kwargs['start_date'], kwargs['initial_capital'])
            else:
                return NaivePortfolio(kwargs['data_handler'], kwargs['event_queue'], kwargs['start_date'])

    @abstractmethod
    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the portfolio logic.
        """
        raise NotImplementedError("Should implement update_signal()")

    @abstractmethod
    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings
        from a FillEvent.
        """
        raise NotImplementedError("Should implement update_fill()")
