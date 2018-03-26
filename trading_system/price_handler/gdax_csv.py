import os
import os.path

import pandas as pd

from .base import BasePriceHandler, SymbolError
from ..events import MarketEvent
from time import gmtime, strftime


class GdaxCsvPriceHandler(BasePriceHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" price bar in a manner identical to a live
    trading interface.
    """

    def __init__(self, event_queue, csv_dir, symbol_list):
        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        It will be assumed that all files are of the form
        'symbol.csv', where symbol is a string in the list.

        symbol_data is a pandas dataframe constructed directly from the csv file containing all
        of the available data for that symbol.

        latest_symbol_data is a formatted dataframe constructed one at a time from new bars that
        get added to it from symbol_data.

        Args:
            event_queue: The EventQueue object
            csv_dir: Absolute directory path to the CSV files
            symbol_list: A list of symbol strings
        """
        self.event_queue = event_queue
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the latest N bars from the latest symbol data dict,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            raise SymbolError("That symbol is not available in the historical data set.")
        else:
            return bars_list[-N:]

    def update_bars(self):
        """
        Pushes the latest price bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = self._get_new_bar(symbol)
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.event_queue.put(MarketEvent())

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """
        combined_index = None
        for symbol in self.symbol_list:
            self._load_csv_file(symbol)
            combined_index = self._combine_index(symbol, combined_index)
            self._set_latest_symbol_data_to_none(symbol)
        self._reindex_dataframes(combined_index)

    def _load_csv_file(self, symbol):
        """Load the CSV file, indexed on time."""
        csv_file = os.path.join(self.csv_dir, '{}.csv'.format(symbol))
        self.symbol_data[symbol] = pd.read_csv(csv_file, index_col=0)

    def _combine_index(self, symbol, combined_index):
        """Combine the index to pad forward values."""
        if combined_index is None:
            combined_index = self.symbol_data[symbol].index
        else:
            combined_index.union(self.symbol_data[symbol].index)
        return combined_index

    def _set_latest_symbol_data_to_none(self, symbol):
        self.latest_symbol_data[symbol] = []

    def _reindex_dataframes(self, combined_index):
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method='pad').iterrows()

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


