import unittest
import os

from config import TestingConfig


class TestDataDir(unittest.TestCase):

    def setUp(self):
        config = TestingConfig()
        data_dir = config.DATA_DIR
        csv_path_template = os.path.join(data_dir, '{}.csv')
        symbols = config.SYMBOLS
        self.csv_files = {symbol: csv_path_template.format(symbol) for symbol in symbols}

    def test_csv_files_exist_for_each_symbol(self):
        for symbol, csv_file in self.csv_files.items():
            self.assertTrue(os.path.exists(csv_file), "The {}.csv file no longer exists.".format(symbol))


if __name__ == '__main__':
    unittest.main()

