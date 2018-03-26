from .base import BasePriceHandler, SymbolError
from .gdax_csv import GdaxCsvPriceHandler

from enum import Enum

DataType = Enum('DataType', 'GDAX_CSV')


def create(data_type, *args, **kwargs):
    if data_type == DataType.GDAX_CSV:
        return GdaxCsvPriceHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid data handler.'.format(data_type))
