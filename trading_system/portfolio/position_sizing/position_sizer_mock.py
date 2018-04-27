class PositionSizerMock:

    def __init__(self):
        pass

    def size_order(self, portfolio, initial_order):
        """
        This PositionSizerMock object simply modifies the quantity
        to be 100 of any share transacted.
        """
        initial_order.quantity = 100
        return initial_order
