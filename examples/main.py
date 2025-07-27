import numpy as np
import pandas as pd
import datetime as dt

from BacktestingEngine.core.market import SingleInstrumentMarket
from BacktestingEngine.core.typedefs import Symbol
from BacktestingEngine.core.engine import BacktestingEngine
from BacktestingEngine.core.execution import SlippageModel
from BacktestingEngine.core.portfolio import Portfolio
from BacktestingEngine.core.strategy import Strategy, Signal
from BacktestingEngine.core.typedefs import TradeSide
from core.indicator import SMA


class MyFirstStrategy(Strategy):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.sma16 = SMA(16)
        self.sma64 = SMA(64)

    def on_data(self, timestamp: pd.Timestamp, value) -> Signal:

        """go long the asset"""
        return Signal(
            timestamp,
            self.symbol,
            TradeSide.BUY,
            1
        )


def main():
    np.random.seed(52)
    initial_capital = 10000
    symbol = "AAPL"
    date = dt.datetime.today().date()
    length = 200
    date_range = pd.date_range(date + dt.timedelta(days=-length),date)
    prices = np.random.randint(100,400,(length+1,1))
    data = pd.DataFrame(prices, columns=["price"],index=date_range)
    execution_model = SlippageModel(1000)
    market = SingleInstrumentMarket(
        symbol, data, execution_model
    )
    portfolio = Portfolio(initial_capital)
    strategy = MyFirstStrategy(symbol)
    backtester = BacktestingEngine(
        market,
        portfolio,
        strategy
    )

    backtester.run()



if __name__ == "__main__":
    main()