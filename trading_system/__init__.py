import os
import queue

from config import base_dir
from . import price_handler
from . import execution_handlers
from . import portfolios
from . import strategies

# Establish the event queue
events = queue.Queue()
DATA_DIR = os.path.join(base_dir, 'data')
symbol_list = ['BTC']

# Declare the components with respective parameters
# data_handler = data_handlers.create('historic_csv', events, csv_dir, symbol_list)
# execution_handler = execution_handlers.create('simulated', events)
# strategy = strategies.create('buy_and_hold', data_handler, events)
# portfolio = portfolios.create('naive', data_handler, events, )
