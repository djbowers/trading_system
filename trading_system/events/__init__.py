from .market_event import MarketEvent
from .order_event import OrderEvent
from .signal_event import SignalEvent
from .fill_event import FillEvent


def grab(event_type, *args, **kwargs):
    if event_type == 'market':
        return MarketEvent()
    elif event_type == 'signal':
        return SignalEvent(*args, **kwargs)
    elif event_type == 'order':
        return OrderEvent(*args, **kwargs)
    elif event_type == 'fill':
        return FillEvent(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid event type.'.format(event_type))
