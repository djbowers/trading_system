from abc import ABCMeta
from enum import Enum


class Event:
    """
    Event is a base class providing an interface for all subsequent
    (inherited) events, that will trigger further events in the
    trading infrastructure.
    """

    __metaclass__ = ABCMeta
    type = None


class EventType(Enum):
    MARKET = 1
    SIGNAL = 2
    ORDER = 3
    FILL = 4
