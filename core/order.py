import pandas as pd
from attr import dataclass

from BacktestingEngine.core.typedefs import Symbol, Price, Quantity, OrderType, TradeSide


@dataclass
class Order:
    """ Data class for order"""
    timestamp: pd.Timestamp
    symbol: Symbol
    order_type: OrderType
    side: TradeSide
    quantity: Quantity
    price: Price = None

    def __str__(self):
        return f"Order({self.timestamp}, {self.symbol} ,{self.order_type}, {self.side}, qty:{self.quantity}, price:{self.price})"


class Trade:
    def __init__(
            self,
            timestamp: pd.Timestamp,
            symbol: Symbol,
            order_type: OrderType,
            side: TradeSide,
            quantity: int,
            filled: bool,
            execution_price: Price = None
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        self.quantity = quantity
        self.filled = filled
        self.execution_price = execution_price

    def log(self):
        pass
