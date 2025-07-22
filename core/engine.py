from abc import ABC, abstractmethod

import pandas as pd

from BacktestingEngine.core.market import Market
from BacktestingEngine.core.strategy import Strategy

class AbstractBacktestingEngine(ABC):
    """ Abstract Backtesting engine class """
    @abstractmethod
    def run(self):
        pass

class BacktestingEngine:

    def __init__(self, market: Market, strategy: Strategy):
        self.market = market
        self.strategy = strategy

    def run(self, *args, **kwargs):
        timestamps: list[pd.Timestamp] = self.market.get_timestamps()
        for timestamp in timestamps:
            self.strategy.signal()