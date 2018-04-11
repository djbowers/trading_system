import unittest

from backtests import sample_backtest
from config import TestingConfig


class TestSampleBacktest(unittest.TestCase):

    def test_that_script_executes(self):
        sample_backtest.run(TestingConfig())
