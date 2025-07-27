from typing import Optional

import numpy as np
import pandas as pd

from BacktestingEngine.core.engine import BacktestingEngine
from BacktestingEngine.core.execution import SlippageModel
from BacktestingEngine.core.market import SingleInstrumentMarket
from BacktestingEngine.core.portfolio import Portfolio
from BacktestingEngine.core.strategy import Strategy, Signal
from BacktestingEngine.core.typedefs import Symbol
from core.indicator import SMA, ZScore


class MyFirstStrategy(Strategy):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.sma16 = SMA(4)
        self.sma64 = SMA(16)
        self.zscore = ZScore(30)

    def on_data(self, timestamp: pd.Timestamp, value) -> Optional[Signal]:
        sma16_val = self.sma16.get_value()
        sma64_val = self.sma64.get_value()
        zscore = self.zscore.get_value()
        if sma16_val and sma64_val and zscore:
            # if zscore <-0.6:
            #     sig_strength = 0.5
            # elif zscore > 0.2:
            #     sig_strength = 0
            # else:
            #     sig_strength = 0

            sig_strength = 1 if sma16_val > sma64_val else 0

            return Signal(
                timestamp,
                self.symbol,
                sig_strength
            )


def main():
    np.random.seed(52)
    initial_capital = 1000000
    symbol = "Snp"
    # date = dt.datetime.today().date()
    # length = 200
    # date_range = pd.date_range(date + dt.timedelta(days=-length),date)
    # prices = np.random.randint(100,400,(length+1,1))
    # data = pd.DataFrame(prices, columns=["price"],index=date_range)
    data = pd.read_csv("data/S&P 500 Historical Results Price Data.csv")
    data = data[["Date", "Price"]].set_index("Date")
    data.index = pd.to_datetime(data.index)
    data["Price"] = data["Price"].map(lambda x: float(x.replace(",", "")))
    execution_model = SlippageModel(0.0)
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
