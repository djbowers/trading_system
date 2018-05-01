from decimal import Decimal

from trading_system.event import FillEvent, MarketEvent
from .position import Position, DOLLAR, CRYPTO


class Portfolio:

    def __init__(self, cash=0.0):
        self.positions = {}
        self._init_cash = Decimal(cash).quantize(DOLLAR)

    def add_new_fill(self, fill: FillEvent):
        if fill.symbol not in self.positions.keys():
            self.positions[fill.symbol] = Position(fill)
        else:
            self.positions[fill.symbol].add_new_fill(fill)

    def update_market_value(self, market: MarketEvent):
        for symbol, bars in market.symbol_data.items():
            latest_bar = bars[-1]
            if symbol in self.positions.keys():
                self.positions[symbol].update_market_value(latest_bar)

    # Portfolio Value

    @property
    def cash(self):
        return (self._init_cash - self.cost_basis).quantize(DOLLAR)

    @property
    def market_value(self):
        return Decimal(
            sum([position.market_value for position in self.positions.values()])
        ).quantize(DOLLAR)

    @property
    def equity(self):
        return (self.cash + self.market_value).quantize(DOLLAR)

    # Tax Accounting

    @property
    def fees(self):
        return Decimal(
            sum([position.fees for position in self.positions.values()])
        ).quantize(DOLLAR)

    @property
    def cost_basis(self):
        return Decimal(
            sum([position.cost_basis for position in self.positions.values()])
        ).quantize(DOLLAR)

    # P&L Calculations

    @property
    def total_pnl(self):
        return (self.realized_pnl + self.unrealized_pnl).quantize(DOLLAR)

    @property
    def realized_pnl(self):
        return Decimal(
            sum([position.realized_pnl for position in self.positions.values()])
        ).quantize(DOLLAR)

    @property
    def unrealized_pnl(self):
        return Decimal(
            sum([position.unrealized_pnl for position in self.positions.values()])
        ).quantize(DOLLAR)
