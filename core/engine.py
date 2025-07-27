from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from BacktestingEngine.core.market import Market
from BacktestingEngine.core.order import Order, Trade
from BacktestingEngine.core.portfolio import Portfolio
from BacktestingEngine.core.strategy import Strategy, Signal
from core.indicator import PriceBasedIndicator


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
        self.diagnostics = pd.DataFrame()
    def run(self, *args, **kwargs):
        timestamps: List[pd.Timestamp] = self.market.get_timestamps()

        vals = []

        for timestamp in timestamps:
            current_price = self.market.get_price(timestamp)
            # Warms up Indicator objects in strategy
            self.update_strategy_indicators(current_price)
            signal: Signal = self.strategy.on_data(timestamp,current_price)
            order: Optional[Order] = self.portfolio.generate_orders(signal, current_price)
            # Only try to fill nonzero orders
            if order:
                trade: Trade = self.market.execute_order(timestamp, order)
                self.portfolio.update_positions(trade)
            self.portfolio.mark_to_market(current_price)

            pnl = self.portfolio.get_unrealised_pnl()
            portfolio_value = self.portfolio.get_portfolio_value()
            vals.append([current_price,pnl,portfolio_value])

        self.diagnostics = pd.DataFrame(vals, columns=["price","pnl","portfolio_val"], index=timestamps)
        print("done")

    def update_strategy_indicators(self, value):
        """ Helper class to look for Indicator objects that need a warmup
            and update them (This should be extendable to other bells and whistles
            I might add later on)
        """
        for member_name in  self.strategy.__dict__:
            if isinstance(self.strategy.__dict__[member_name],PriceBasedIndicator):
                if hasattr(self.strategy.__dict__[member_name], "update"):
                    self.strategy.__dict__[member_name].update(value)


