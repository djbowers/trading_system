from abc import ABCMeta


class Event:
    """
    Event is a base class providing an interface for all subsequent
    (inherited) events, that will trigger further events in the
    trading infrastructure.
    """

    __metaclass__ = ABCMeta
