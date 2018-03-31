from abc import ABCMeta, abstractmethod
from trading_system.events import SignalEvent, FillEvent


class PortfolioHandler:
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e. 1-min, 5-min, 15-min, 1-hr, 4-hr, or daily.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update_signal(self, event: SignalEvent):
        """
        Acts on a SignalEvent to generate new orders based on the portfolio logic,
        producing an OrderEvent.
        """
        raise NotImplementedError("Should implement update_signal()")

    @abstractmethod
    def update_fill(self, event: FillEvent):
        """
        Updates the portfolio current positions and holdings from a FillEvent.
        """
        raise NotImplementedError("Should implement update_fill()")
