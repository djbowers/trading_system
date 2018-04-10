import unittest
from trading_system.execution import ExecutionHandler


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.execution_handler = ExecutionHandler()

    def test_for_error_on_execute_order(self):
        self.assertRaises(NotImplementedError, self.execution_handler.execute_order, None)
