import unittest
import os

from . import TEST_DATA_DIR, SYMBOLS


class TestDataDir(unittest.TestCase):

    def setUp(self):
        csv_path_template = os.path.join(TEST_DATA_DIR, '{}.csv')
        self.csv_files = {symbol: csv_path_template.format(symbol) for symbol in SYMBOLS}

    def test_data_files_exist(self):
        """Test that CSV files exist for each symbol in SYMBOLS."""
        for symbol, csv_file in self.csv_files.items():
            self.assertTrue(os.path.exists(csv_file), "The {}.csv file no longer exists.".format(symbol))


if __name__ == '__main__':
    unittest.main()

