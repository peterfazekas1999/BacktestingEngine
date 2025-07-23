from dataclasses import dataclass

import pandas as pd

from BacktestingEngine.core.order import Order, Trade
from BacktestingEngine.core.signal import Signal
from BacktestingEngine.core.typedefs import Symbol, TradeSide

@dataclass
class PositionLot:
    timestamp: pd.Timestamp
    quantity: float
    price: float

class Position:
    def __init__(self, symbol):
        self.symbol = symbol
        self.position_lots: list[PositionLot] = []
    def add_position_lot(self, lot: PositionLot):
        self.position_lots.append(lot)
    def close_position_lot(self, quantity: float):
        # implement a FIFO or LIFO
        pass


class Portfolio:
    def __init__(
            self,
            initial_capital: float):
        self.initial_capital = initial_capital
        self.current_holdings: float = 0.0
        self.available_capital: float = initial_capital
        self.positions: dict[Symbol,Position] = {}
        self.orders: dict[Symbol, list[Order]] = {}
        self.trades: dict[Symbol, list[Trade]] = {}
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0
    def generate_orders(self, signal: Signal):
        pass

    def update_holding(self):
        pass


