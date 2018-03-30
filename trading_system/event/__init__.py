from .base import BaseEvent
from .fill import FillEvent
from .market import MarketEvent
from .order import OrderEvent
from .signal import SignalEvent
from .type import EventType


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
