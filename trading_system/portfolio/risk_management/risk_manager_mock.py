from trading_system.event import OrderEvent


class RiskManagerMock:

    def __init__(self):
        pass

    def refine_orders(self, portfolio, sized_order):
        """
        This RiskManagerMock object simply lets the sized order
        through, creates the corresponding OrderEvent object
        and adds it to a list.
        """
        order_event = OrderEvent(
            symbol=sized_order.symbol,
            direction=sized_order.direction,
            quantity=sized_order.quantity,
            order_type='MKT'  # TODO: implement limit order types
        )

        return [order_event]
