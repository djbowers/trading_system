import unittest
from trading_system import execution
from trading_system.events import EventQueue, OrderEvent, FillEvent


class TestExecutionHandler(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.execution_handler = execution.SimulatedExecutionHandler(self.events)

    def test_execute_order_adds_fill_event(self):
        order_event = OrderEvent('BTC', 'MKT', 1, 'BUY')
        self.execution_handler.execute_order(order_event)
        fill_event = self.events.maybe_get_next_event()
        self.assertIsInstance(fill_event, FillEvent,
                              "The correct event type was not added to the queue.")


if __name__ == '__main__':
    unittest.main()
