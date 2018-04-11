import unittest
from trading_system.engine import Engine


class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.engine = Engine()

    def test_for_error_on_start(self):
        self.assertRaises(NotImplementedError, self.engine.run)
