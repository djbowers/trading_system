from abc import ABCMeta, abstractmethod
from trading_system.event import SignalEvent, FillEvent


class PortfolioHandler:
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e. 1-min, 5-min, 15-min, 1-hr, 4-hr, or daily.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update_on_signal(self, event: SignalEvent):
        """
        Acts on a SignalEvent to generate new orders based on the portfolio logic,
        producing an OrderEvent.
        """
        raise NotImplementedError

    @abstractmethod
    def update_on_fill(self, event: FillEvent):
        """
        Updates the portfolio current positions and holdings from a FillEvent.
        """
        raise NotImplementedError

    @abstractmethod
    def update_on_market(self, event: FillEvent):
        """
        Moves current positions and current holdings into all positions
        and all holdings, respectively, adding the timeindex and market
        value from the market event.
        """
        raise NotImplementedError
