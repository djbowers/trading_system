#!/usr/bin/env python

from datetime import datetime

from trading_system.data import GDAXCSVDataHandler
from trading_system.engine import BacktestingEngine
from trading_system.event import EventQueue
from trading_system.execution import SimulatedExecutionHandler
from trading_system.portfolio import NaivePortfolioHandler
from trading_system.strategy import BuyAndHoldStrategy
from config import DevelopmentConfig

events = EventQueue()
csv_dir = DevelopmentConfig.DATA_DIR
symbols = DevelopmentConfig.SYMBOLS

data_handler = GDAXCSVDataHandler(events, symbols, csv_dir)
execution_handler = SimulatedExecutionHandler(events)
strategy = BuyAndHoldStrategy(events, symbols)
portfolio_handler = NaivePortfolioHandler(events, symbols, datetime.utcnow())

engine = BacktestingEngine(events, data_handler, strategy, portfolio_handler, execution_handler)

engine.start()
