from .base import BasePriceHandler
from .gdax_csv import GDAXCSVPriceHandler
from .type import PriceType


def create_handler(data_type, *args, **kwargs):
    if data_type == PriceType.GDAX_CSV:
        return GDAXCSVPriceHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid data handler.'.format(data_type))
