import unittest
from trading_system.strategy import Strategy


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.strategy = Strategy()

    def test_for_error_on_calculate_signals(self):
        self.assertRaises(NotImplementedError, self.strategy.calculate_signals, None)
