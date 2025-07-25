from abc import ABC, abstractmethod

import pandas as pd

from BacktestingEngine.core.signal import Signal


class Strategy(ABC):

    @abstractmethod
    def on_data(self,timestamp: pd.Timestamp, value) -> Signal:
        pass
