from abc import ABC, abstractmethod

import pandas as pd

from BacktestingEngine.core.signal import Signal
from core.indicator import PriceBasedIndicator
from core.logger import logger


class Strategy(ABC):

    def generate_signal(self, timestamp: pd.Timestamp, value):
        """ Backtesting Engine entry point, should not be overriden."""

        self.update_strategy_indicators(value)
        signal = self.on_data(timestamp, value)
        if signal:
            logger.info(f"Signal Generated: {signal}")
        return signal

    def update_strategy_indicators(self, value):
        """ Helper class to look for Indicator objects that need a warmup
            and update them (This should be extendable to other bells and whistles
            I might add later on)
        """
        for member_name in self.__dict__:
            if isinstance(self.__dict__[member_name], PriceBasedIndicator):
                if hasattr(self.__dict__[member_name], "update"):
                    self.__dict__[member_name].update(value)

    @abstractmethod
    def on_data(self, timestamp: pd.Timestamp, value) -> Signal:
        """ Override in Subclasses"""
        pass
