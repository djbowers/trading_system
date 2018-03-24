import datetime

from .event import FillEvent
from ..execution import ExecutionHandler


class SimulatedExecutionHandler(ExecutionHandler):
    """
    The simulated execution handler simply converts all order
    objects into their equivalent fill objects automatically
    without latency, slippage or fill-ratio issues.

    This allows a straightforward "first go" test of any strategy,
    before implementation with a more sophisticated execution
    handler.
    """

    def __init__(self, event_queue):
        """
        Initialises the handler, setting the event queues
        up internally.

        Args:
            event_queue: The EventQueue object
        """
        self.event_queue = event_queue

    def execute_order(self, event):
        """
        Simply converts Order objects into Fill objects naively,
        i.e. without any latency, slippage or fill ratio problems.

        Args:
            event: Contains an Event object with order information.
        """
        if event.type == 'ORDER':
            fill_event = FillEvent(datetime.datetime.utcnow(), event.symbol,
                                   'BTC', event.quantity, event.direction, None)
            self.event_queue.put(fill_event)
