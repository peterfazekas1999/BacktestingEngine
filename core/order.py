from enum import Enum
from BacktestingEngine.core.typedefs import Symbol, Price, Quantity, OrderType, TradeSide
import pandas as pd
from attr import dataclass

@dataclass
class Order:
    """ Data class for order"""
    timestamp: pd.Timestamp
    symbol: Symbol
    order_type: OrderType
    side: TradeSide
    quantity: Quantity
    price: Price = None

class Trade:
    def __init__(
        self,
        timestamp: pd.Timestamp,
        symbol: Symbol,
        order_type: OrderType,
        side: TradeSide,
        quantity: int,
        filled: bool,
        price: Price = None
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        self.quantity = quantity
        self.filled = filled
        self.price = price

    def log(self):
        pass
