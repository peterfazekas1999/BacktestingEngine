from abc import abstractmethod, ABC

import pandas as pd
import datetime as dt


class Market(ABC):
    """Abstract base class for market"""
    @abstractmethod
    def get_timestamps(self):
        pass

    @abstractmethod
    def get_price(self, timestamp: dt.datetime):
        pass

    @abstractmethod
    def execute_order(self, order):
        pass


class SingleInstrumentMarket(Market):
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.symbol: str = symbol
        self.timestamps: pd.Timestamp = data.index

    def get_timestamps(self):
        return self.timestamps

    def get_price(self, timestamp: pd.Timestamp):
        return self.data.loc[timestamp]

    def execute_order(self, order):
        # order.execute(..)
        pass



