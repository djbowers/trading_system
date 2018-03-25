from .base_data_handler import BaseDataHandler
from .historic_csv_data_handler import HistoricCSVDataHandler


def create(data_type, *args, **kwargs):
    if data_type == 'historic_csv':
        return HistoricCSVDataHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid data handler.'.format(data_type))
