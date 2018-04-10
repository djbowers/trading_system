import unittest
from trading_system import execution
from trading_system.event import EventQueue, OrderEvent, EventType


class TestSimulatedExecutionHandler(unittest.TestCase):

    def setUp(self):
        self.events = EventQueue()
        self.execution_handler = execution.SimulatedExecutionHandler(self.events)

    def test_execute_order_adds_fill_event(self):
        order_event = OrderEvent('BTC', 'MKT', 1, 'BUY')
        self.execution_handler.execute_order(order_event)
        fill_event = self.events.get_next_event()
        self.assertEqual(fill_event.type, EventType.FILL)


if __name__ == '__main__':
    unittest.main()
