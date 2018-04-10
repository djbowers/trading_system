from abc import ABCMeta, abstractmethod


class Engine:
    """
    The Engine is what ties all of the other components of the system together. It
    is what powers the trading system, just like an engine powers a car.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """
        Start the trading engine.
        """
        raise NotImplementedError
