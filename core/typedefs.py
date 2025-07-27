from enum import Enum

type Bps = float  # basis points
type Price = float
type Quantity = int
type Symbol = str


class OrderType(Enum):
    MARKET = "MarketOrder"


class TradeSide(Enum):
    BUY = "Buy"
    SELL = "Sell"
