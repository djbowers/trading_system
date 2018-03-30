from datetime import datetime

from trading_system.events import FillEvent, OrderEvent, EventQueue
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

    def __init__(self, event_queue: EventQueue):
        self.events = event_queue

    def execute_order(self, event: OrderEvent):
        fill_event = FillEvent(datetime.utcnow(), event.symbol, 'BTC', event.quantity, event.direction, None)
        self.events.add_event(fill_event)
