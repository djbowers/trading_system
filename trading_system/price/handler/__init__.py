from enum import Enum

from .base import BasePriceHandler
from .csv.gdax import GdaxCsvPriceHandler


def create_handler(data_type, *args, **kwargs):
    if data_type == DataType.GDAX_CSV:
        return GdaxCsvPriceHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid data handler.'.format(data_type))


class DataType(Enum):
    GDAX_CSV: 1


class SymbolError(KeyError):
    pass
