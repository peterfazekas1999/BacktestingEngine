import pandas as pd

from BacktestingEngine.core.typedefs import Symbol


class Signal:
    def __init__(self,
                 timestamp: pd.Timestamp,
                 symbol: Symbol,
                 strength: float,
                 ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.strength = strength

    def __str__(self):
        return f"Signal({self.timestamp}, {self.symbol},{self.strength})"
