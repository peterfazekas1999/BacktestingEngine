from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from BacktestingEngine.core.market import Market
from BacktestingEngine.core.order import Order, Trade
from BacktestingEngine.core.portfolio import Portfolio
from BacktestingEngine.core.strategy import Strategy, Signal


class AbstractBacktestingEngine(ABC):
    """ Abstract Backtesting engine class """

    @abstractmethod
    def run(self):
        pass


class BacktestingEngine(AbstractBacktestingEngine):
    """
        Main core logic of the engine

        :param: market - contains the data, can execute orders
        :param: portfolio - contains current holdings, calculates pnl, generates orders
        from strategy signals and feeds them to the market
        :param: strategy - generates signals

    """

    def __init__(self,
                 market: Market,
                 portfolio: Portfolio,
                 strategy: Strategy):
        self.market = market
        self.strategy = strategy
        self.portfolio = portfolio

    def run(self, *args, **kwargs):
        timestamps: List[pd.Timestamp] = self.market.get_timestamps()
        for timestamp in timestamps:
            current_price = self.market.get_price(timestamp)
            # Get strategy signals
            signal: Optional[Signal] = self.strategy.generate_signal(timestamp, current_price)

            order: Optional[Order] = self.portfolio.generate_orders(signal, current_price)
            # Only try to fill nonzero orders
            if order:
                trade: Trade = self.market.execute_order(timestamp, order)
                self.portfolio.update_positions(trade)

            # Mark portfolio to market
            self.portfolio.mark_to_market(current_price)
