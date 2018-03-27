from enum import Enum

from .fill import FillEvent
from .market import MarketEvent
from .order import OrderEvent
from .signal import SignalEvent


def create_event(event_type, *args, **kwargs):
    if event_type == EventType.MARKET:
        return MarketEvent()
    elif event_type == EventType.SIGNAL:
        return SignalEvent(*args, **kwargs)
    elif event_type == EventType.ORDER:
        return OrderEvent(*args, **kwargs)
    elif event_type == EventType.FILL:
        return FillEvent(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid event type.'.format(event_type))


class EventType(Enum):
    MARKET = 1
    SIGNAL = 2
    ORDER = 3
    FILL = 4
