from abc import abstractmethod
from collections import deque
from typing import Deque

import numpy as np

from BacktestingEngine.core.typedefs import Price


class PriceBasedIndicator:
    def __init__(self,
                 window_size: int,
                 ignore_warmup: bool = False
                 ):
        self.window_size = window_size
        self._is_ready: bool = ignore_warmup
        self.data: Deque[Price] = deque(maxlen=window_size)

    def is_ready(self):
        return self._is_ready

    def update(self, value: Price):
        self.data.append(value)
        if len(self.data) == self.window_size:
            self._is_ready = True
        self._calculate()

    @abstractmethod
    def _calculate(self):
        """ override in subclasses. """
        pass


class SMA(PriceBasedIndicator):
    def __init__(self, window_size: int, ignore_warmup: bool = False):
        super().__init__(window_size, ignore_warmup)
        self.current_value = None

    def _calculate(self):
        if self.is_ready():
            self.current_value = sum(self.data) / self.window_size

    def get_value(self):
        return self.current_value


class ZScore(PriceBasedIndicator):
    def __init__(self, window_size: int, ignore_warmup: bool = False):
        super().__init__(window_size, ignore_warmup)
        self.current_value = None

    def _calculate(self):
        if self.is_ready():
            mu = sum(self.data) / self.window_size
            std = np.sqrt(sum([(x - mu) ** 2 for x in self.data]) / (self.window_size - 1))
            self.current_value = (self.data[-1] - mu) / std

    def get_value(self):
        return self.current_value
