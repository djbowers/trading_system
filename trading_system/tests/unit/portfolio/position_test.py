import unittest
from decimal import Decimal

from trading_system.data import PriceBar
from trading_system.event import FillEvent
from trading_system.portfolio import Position


class TestLongPosition(unittest.TestCase):

    def setUp(self):
        first_fill = FillEvent('0:00', 'BTC', 10, 'BUY', 1000.00, 'GDAX', fee=50.00)
        self.second_fill = FillEvent('1:00', 'BTC', 20, 'BUY', 1000.00, 'GDAX', fee=100.00)
        self.position = Position(first_fill)

    def test_cost_basis(self):
        self.assertEqual(self.position.cost_basis, Decimal("10050"))

    def test_avg_buy_price(self):
        self.assertEqual(self.position.avg_buy_price, Decimal("1000"))

    def test_avg_sell_price(self):
        self.assertEqual(self.position.avg_sell_price, Decimal("0"))

    def test_avg_open_price(self):
        self.assertEqual(self.position.avg_open_price, Decimal("1000"))

    def test_total_open_price(self):
        self.assertEqual(self.position.total_open_price, Decimal("10000"))

    def test_fees(self):
        self.assertEqual(self.position.fees, Decimal("50"))

    def test_fees_with_second_fill(self):
        self.position.add_new_fill(self.second_fill)
        self.assertEqual(self.position.fees, Decimal("150"))

    def test_quantities(self):
        self.assertEqual(self.position.qty_bought, Decimal("10"))
        self.assertEqual(self.position.qty_sold, Decimal("0"))
        self.assertEqual(self.position.qty_open, Decimal("10"))

    def test_quantities_with_second_fill(self):
        self.position.add_new_fill(self.second_fill)
        self.assertEqual(self.position.qty_bought, Decimal("30"))
        self.assertEqual(self.position.qty_sold, Decimal("0"))
        self.assertEqual(self.position.qty_open, Decimal("30"))

    def test_realized_pnl(self):
        self.assertEqual(self.position.realized_pnl, Decimal("0"))

    def test_update_market_value_with_invalid_symbol(self):
        price_bar = PriceBar("0:00", 0, 0, 0, 0, 0, 'INVALID')
        self.assertRaises(ValueError, self.position.update_market_value, price_bar)

    def test_add_new_fill_with_invalid_symbol(self):
        fill = FillEvent('0:00', 'INVALID', 10, 'BUY', 1000.00, 'GDAX', fee=50.00)
        self.assertRaises(ValueError, self.position.add_new_fill, fill)

    def test_add_new_fill_with_invalid_exchange(self):
        fill = FillEvent('0:00', 'BTC', 10, 'BUY', 1000.00, 'INVALID', fee=50.00)
        self.assertRaises(ValueError, self.position.add_new_fill, fill)

    def test_direction_is_long(self):
        self.assertEqual(self.position.direction, "LONG")

    def test_polarity_is_positive(self):
        self.assertEqual(self.position.polarity, 1)

    def test_status_is_open(self):
        self.assertEqual(self.position.status, "OPEN")


class TestShortPosition(unittest.TestCase):

    def setUp(self):
        first_fill = FillEvent('0:00', 'BTC', 10, 'SELL', 1000.00, 'GDAX', fee=50.00)
        self.second_fill = FillEvent('1:00', 'BTC', 20, 'SELL', 1000.00, 'GDAX', fee=100.00)
        self.position = Position(first_fill)

    def test_cost_basis(self):
        self.assertEqual(self.position.cost_basis, Decimal("-10050"))

    def test_avg_buy_price(self):
        self.assertEqual(self.position.avg_buy_price, Decimal("0"))

    def test_avg_sell_price(self):
        self.assertEqual(self.position.avg_sell_price, Decimal("1000"))

    def test_avg_open_price(self):
        self.assertEqual(self.position.avg_open_price, Decimal("1000"))

    def test_total_open_price(self):
        self.assertEqual(self.position.total_open_price, Decimal("-10000"))

    def test_quantities(self):
        self.assertEqual(self.position.qty_sold, Decimal("10"))
        self.assertEqual(self.position.qty_bought, Decimal("0"))
        self.assertEqual(self.position.qty_open, Decimal("-10"))

    def test_quantities_with_second_fill(self):
        self.position.add_new_fill(self.second_fill)
        self.assertEqual(self.position.qty_sold, Decimal("30"))
        self.assertEqual(self.position.qty_bought, Decimal("0"))
        self.assertEqual(self.position.qty_open, Decimal("-30"))

    def test_direction_is_short(self):
        self.assertEqual(self.position.direction, "SHORT")

    def test_polarity_is_negative(self):
        self.assertEqual(self.position.polarity, -1)


class TestMixedPosition(unittest.TestCase):
    """
    Based off calculations found at the following URL:
    https://www.tradingtechnologies.com/help/fix-adapter-reference/pl-calculation-algorithm/understanding-pl-calculations/
    """

    def setUp(self):
        fee = 0.00
        fill_1 = FillEvent('1:00', 'BTC', 12, 'BUY', 100.0, 'GDAX', fee=fee)
        fill_2 = FillEvent('2:00', 'BTC', 17, 'BUY', 99.0, 'GDAX', fee=fee)
        fill_3 = FillEvent('3:00', 'BTC', 9, 'SELL', 101.0, 'GDAX', fee=fee)
        fill_4 = FillEvent('4:00', 'BTC', 4, 'SELL', 105.0, 'GDAX', fee=fee)
        fill_5 = FillEvent('5:00', 'BTC', 3, 'BUY', 103.0, 'GDAX', fee=fee)
        self.position = Position(fill_1)
        self.position.add_new_fill(fill_2)
        self.position.add_new_fill(fill_3)
        self.position.add_new_fill(fill_4)
        self.position.add_new_fill(fill_5)
        self.price_bar = PriceBar("6:00", 100.0, 95.0, 110.0, 105.0, 100, 'BTC')

    def test_total_buy_qty(self):
        self.assertEqual(self.position.qty_bought, Decimal("32"))

    def test_total_sell_qty(self):
        self.assertEqual(self.position.qty_sold, Decimal("13"))

    def test_avg_buy_price(self):
        self.assertEqual(self.position.avg_buy_price, Decimal("99.75"))

    def test_avg_sell_price(self):
        self.assertEqual(self.position.avg_sell_price, Decimal("102.23"))

    def test_avg_open_price(self):
        self.assertEqual(self.position.avg_open_price, Decimal("98.05"))

    def test_market_value(self):
        self.assertEqual(self.position.market_value, Decimal("1957.00"))

    def test_realized_pnl(self):
        self.assertEqual(self.position.realized_pnl, Decimal("47.12"))

    def test_unrealized_pnl(self):
        self.position.update_market_value(self.price_bar)
        self.assertEqual(self.position.unrealized_pnl, Decimal("132.05"))

    def test_total_pnl(self):
        self.position.update_market_value(self.price_bar)
        self.assertEqual(self.position.total_pnl, Decimal("179.17"))

    def test_market_value_after_update(self):
        self.position.update_market_value(self.price_bar)
        self.assertEqual(self.position.market_value, Decimal("1995.00"))


class TestClosedPosition(unittest.TestCase):

    def setUp(self):
        first_fill = FillEvent('0:00', 'BTC', 10, 'BUY', 1000.00, 'GDAX', fee=0.0)
        second_fill = FillEvent('1:00', 'BTC', 10, 'SELL', 1100.00, 'GDAX', fee=0.0)
        self.position = Position(first_fill)
        self.position.add_new_fill(second_fill)

    def test_direction_is_na(self):
        self.assertEqual(self.position.direction, "N/A")

    def test_polarity_is_zero(self):
        self.assertEqual(self.position.polarity, 0)

    def test_status_is_closed(self):
        self.assertEqual(self.position.status, "CLOSED")
