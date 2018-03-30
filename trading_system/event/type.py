from enum import Enum


class EventType(Enum):
    MARKET = 1
    SIGNAL = 2
    ORDER = 3
    FILL = 4
