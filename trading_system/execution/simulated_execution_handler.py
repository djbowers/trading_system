import time

from trading_system.event import FillEvent, OrderEvent, EventQueue
from .execution_handler import ExecutionHandler


class SimulatedExecutionHandler(ExecutionHandler):
    """
    The simulated execution handler simply converts all order
    objects into their equivalent fill objects automatically
    without latency, slippage or fill-ratio issues.

    This allows a straightforward "first go" test of any strategy,
    before implementation with a more sophisticated execution
    handler.
    """

    def __init__(self, events: EventQueue):
        self.events = events

    def execute_order(self, event: OrderEvent):
        """Creates a fake FillEvent and adds it to the event queue."""
        fill_event = FillEvent(int(time.time()), event.symbol, event.quantity,
                               event.direction, fill_cost=0, exchange='GDAX')
        self.events.add_event(fill_event)
