from time import gmtime, strftime

import pandas as pd

from trading_system.errors import SymbolError
from trading_system.events import MarketEvent, EventQueue
from .data_handler import DataHandler
import utils


class GDAXCSVDataHandler(DataHandler):
    """
    Designed to read CSV files for each requested symbol from disk and
    provide an interface to obtain the "latest" price bar.
    """

    def __init__(self, events: EventQueue, csv_dir, symbols):
        """
        It will be assumed that all csv files are of the form
        'symbol.csv', where symbol is a string in the list.

        symbol_data:
            Pandas DataFrame constructed directly from the csv file
            containing all of the available data for that symbol

        latest_symbol_data:
            Formatted Pandas DataFrame constructed one at a time
            from new bars that get added to it from symbol_data
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbols = symbols

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def get_latest_bars(self, symbol, num_bars=1):
        """
        Returns the latest num_bars from latest_symbol_data,
        or (num_bars - k) if less k available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            raise SymbolError("That symbol is not available in the historical data set.")
        else:
            return bars_list[-num_bars:]

    def update_bars(self):
        """
        Pushes the latest price bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbols:
            try:
                bar = self._get_new_bar(symbol)
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.add_event(MarketEvent())

    def _get_new_bar(self, symbol):
        """
        Returns the latest price bar from the data feed as a tuple of
        (symbol, datetime, low, high, open, close, volume).
        """
        for bar in self.symbol_data[symbol]:
            time_of_bar = bar[0]
            formatted_time = strftime('%Y-%m-%d %H:%M:%S', gmtime(time_of_bar))

            bar_as_series = bar[1]
            low_of_bar = bar_as_series[0]
            high_of_bar = bar_as_series[1]
            open_of_bar = bar_as_series[2]
            close_of_bar = bar_as_series[3]
            volume_of_bar = bar_as_series[4]

            yield tuple(
                [symbol, formatted_time, low_of_bar, high_of_bar, open_of_bar, close_of_bar, volume_of_bar]
            )

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """
        combined_index = None
        for symbol in self.symbols:

            # Load the CSV file, indexed on time.
            csv_file = utils.join_paths(self.csv_dir, '{}.csv'.format(symbol))
            self.symbol_data[symbol] = pd.read_csv(csv_file, index_col=0)

            # Combine the index to pad forward values.
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)

            # Create key for symbol in latest_symbol_data
            self.latest_symbol_data[symbol] = []

        # Reindex dataframes
        for symbol in self.symbols:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method='pad').iterrows()
