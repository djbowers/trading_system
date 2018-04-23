from decimal import Decimal
from trading_system.data import PriceBar
from trading_system.event import FillEvent


DOLLAR = Decimal("0.00")
CRYPTO = Decimal("0.00000000")


class Position:
    """
    Represents a single round-trip position in an asset. That is, it tracks the
    realised and unrealised profit and loss (PnL) by averaging the multiple "legs"
    of the transaction, inclusive of transaction costs.

    For instance, let's imagine we carry out the following transactions:

    Day 1 - Purchase 100 shares of BTC. Total 100.
    Day 2 - Purchase 200 shares of BTC. Total 300.
    Day 3 - Sell 400 shares of BTC. Total -100.
    Day 4 - Purchase 200 shares of BTC. Total 100.
    Day 5 - Sell 100 shares of BTC. Total 0.

    This constitutes a "round trip".
    """

    def __init__(self, fill: FillEvent):
        """
        Set up the initial "account" of the position to be zero for most
        items, with the exception of the initial purchase/sale.

        Then calculate the initial values and finally update the market
        value of the position.
        """
        self._fills = [fill]

        self.symbol = fill.symbol
        self.exchange = fill.exchange

        self.est_exit_price = Decimal(fill.price).quantize(DOLLAR)

    def update_market_value(self, price_bar: PriceBar):
        """
        The estimated exit price is determined using the closing price of the most recent
        price bar. The market value is then recalculated based on the new exit price, as
        well as all subsequent P&L values.
        """
        if price_bar.symbol == self.symbol:
            self.est_exit_price = Decimal(price_bar.close).quantize(DOLLAR)
        else:
            raise ValueError("The price bar is for a different symbol than the position.")

    def add_new_fill(self, fill: FillEvent):
        """
        Add another "leg" to the position by adding a new fill event. All financial
        data will be recalculated automatically upon adding the fill.
        """
        if fill.symbol == self.symbol and fill.exchange == self.exchange:
            self._fills.append(fill)
            self.est_exit_price = Decimal(fill.price).quantize(DOLLAR)
        else:
            raise ValueError("The fill event is for a different symbol or exchange than the position.")

    # Position Status & Direction

    @property
    def direction(self):
        if self.qty_open > 0:
            return "LONG"
        elif self.qty_open < 0:
            return "SHORT"
        else:
            return "N/A"

    @property
    def polarity(self):
        if self.qty_open > 0:
            return 1
        elif self.qty_open < 0:
            return -1
        else:
            return 0

    @property
    def status(self):
        if self.qty_open == 0:
            return "CLOSED"
        else:
            return "OPEN"

    # Quantity Calculations

    @property
    def qty_bought(self):
        return Decimal(sum([fill.quantity for fill in self._fills if fill.direction == "BUY"])).quantize(CRYPTO)

    @property
    def qty_sold(self):
        return Decimal(sum([fill.quantity for fill in self._fills if fill.direction == "SELL"])).quantize(CRYPTO)

    @property
    def qty_open(self):
        return (self.qty_bought - self.qty_sold).quantize(CRYPTO)

    # Price Calculations

    @property
    def total_buy_price(self):
        return Decimal(sum([Decimal(fill.price) * Decimal(fill.quantity) for fill in self._fills if fill.direction == "BUY"])).quantize(DOLLAR)

    @property
    def total_sell_price(self):
        return Decimal(sum([Decimal(fill.price) * Decimal(fill.quantity) for fill in self._fills if fill.direction == "SELL"])).quantize(DOLLAR)

    @property
    def avg_buy_price(self):
        if self.qty_bought:
            return (self.total_buy_price / self.qty_bought).quantize(DOLLAR)
        else:
            return Decimal("0")

    @property
    def avg_sell_price(self):
        if self.qty_sold:
            return (self.total_sell_price / self.qty_sold).quantize(DOLLAR)
        else:
            return Decimal("0")

    @property
    def total_open_price(self):
        return (self.total_buy_price - self.total_sell_price).quantize(DOLLAR)

    @property
    def avg_open_price(self):
        return (self.total_open_price / self.qty_open).quantize(DOLLAR)

    # Tax Accounting

    @property
    def fees(self):
        return Decimal(sum([Decimal(fill.fee) for fill in self._fills])).quantize(DOLLAR)

    @property
    def cost_basis(self):
        return (self.avg_open_price * self.qty_open + self.polarity * self.fees).quantize(DOLLAR)

    # P&L Calculations

    @property
    def market_value(self):
        return (self.qty_open * self.est_exit_price).quantize(DOLLAR)

    @property
    def total_pnl(self):
        return (self.realized_pnl + self.unrealized_pnl).quantize(DOLLAR)

    @property
    def realized_pnl(self):
        if self.avg_buy_price and self.avg_sell_price:
            return ((self.avg_sell_price - self.avg_buy_price) * self.qty_open).quantize(DOLLAR)
        else:
            return Decimal("0")

    @property
    def unrealized_pnl(self):
        return ((self.est_exit_price - self.avg_open_price) * self.qty_open).quantize(DOLLAR)
