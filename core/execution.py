from abc import ABC, abstractmethod

import pandas as pd

from BacktestingEngine.core.order import Order, Trade
from BacktestingEngine.core.typedefs import Price, TradeSide, Bps
from core.logger import logger


class ExecutionModel(ABC):

    @abstractmethod
    def fill(self, order: Order,timestamp: pd.Timestamp, market_price: Price):
        pass

class PerfectFillModel(ExecutionModel):
    """ Perfect fill model, always execute all quantities at market price"""
    def __init__(self):
        pass

    def fill(self, order: Order,timestamp: pd.Timestamp, market_price: Price):
        # once integrated with brokers feeds or execution models
        # will either return true or false
        # how much was actually executed and at what price
        # for simplicity we now assume all orders are filled exactly at
        # market price successfully with no slippage
        filled = True
        executed_qty = order.quantity
        execution_price = market_price

        return Trade(
            timestamp,
            order.symbol,
            order.order_type,
            order.side,
            executed_qty,
            filled,
            execution_price
        )

class SlippageModel(ExecutionModel):
    """ Simple slippage model, applies a fixed bps spread on all trades

        :param: slippage - enter it in basis points, e.g. 40 for 40bps of slipapge each trade
    """
    def __init__(self, slippage: Bps):
        self.slippage= slippage

    def apply_slippage(self, price: Price, trade_side: TradeSide):
        return (
            price * (1 + self.slippage / 1e4) if trade_side == TradeSide.BUY
                else price * (1 - self.slippage / 1e4)
        )


    def fill(self, order: Order,timestamp: pd.Timestamp, market_price: Price):
        filled = True
        executed_qty = order.quantity
        execution_price = self.apply_slippage(market_price, order.side)
        logger.info(f"Order Filled: {order}")
        return Trade(
            timestamp,
            order.symbol,
            order.order_type,
            order.side,
            executed_qty,
            filled,
            execution_price
        )