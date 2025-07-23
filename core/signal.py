import pandas as pd

from BacktestingEngine.core.typedefs import Symbol, TradeSide


class Signal:
    def __init__(self,
        timestamp: pd.Timestamp,
        symbol: Symbol,
        side: TradeSide,
        strength: float,
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.side = side
        self.strength = strength
