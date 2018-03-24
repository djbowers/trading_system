import os
import queue

from config import basedir
from .data import DataHandler
from .execution import ExecutionHandler
from .portfolio import Portfolio
from .strategy import Strategy

# Establish the event queue
events = queue.Queue()
csv_dir = os.path.join(basedir, 'data')
symbol_list = ['BTC']

# Declare the components with respective parameters
data_handler = DataHandler.create_handler('historic_csv', events=events, csv_dir=csv_dir, symbol_list=symbol_list)
strategy = Strategy.create_new_strategy('buy_and_hold', data_handler=data_handler, events=events)
portfolio = Portfolio.create_new_portfolio('naive', data_handler=data_handler, events=events, )
# broker = ExecutionHandler(..)


execution_handler = ExecutionHandler.create_new_handler('simulated', events=events)
