from collections import deque
from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

from BacktestingEngine.core.logger import logger
from BacktestingEngine.core.order import Order, Trade
from BacktestingEngine.core.signal import Signal
from BacktestingEngine.core.typedefs import Symbol, TradeSide, Price, OrderType


@dataclass
class PositionLot:
    timestamp: pd.Timestamp
    quantity: int
    price: float
    def __str__(self):
        return f"PositionLot({self.timestamp},{self.quantity},{self.price})"

class Position:
    def __init__(self, symbol):
        self.symbol = symbol
        self.position_lots: deque[PositionLot] = deque()
    def add_position_lot(self, lot: PositionLot):
        self.position_lots.append(lot)
    def close_position_lot(self, trade: Trade) -> float:
        # implement FIFO
        # need to report the PnL gain/loss too
        assert trade.side == TradeSide.SELL
        quantity_to_close = trade.quantity
        execution_price = trade.execution_price
        realised_pnl = 0.0
        while quantity_to_close > 0:
            if self.position_lots:
                curr_post_lot: PositionLot = self.position_lots.popleft()
                curr_qty = curr_post_lot.quantity
                quantity_to_close -= curr_qty
                logger.info(f"Closed {self.symbol} position lot {curr_post_lot}")

                # calculate PnL
                realised_pnl += curr_qty * (execution_price - curr_post_lot.price)
            else:
                raise ValueError("Trying to close non-existent positions")
        return realised_pnl

class Portfolio:
    def __init__(
            self,
            initial_capital: float):

        self.holdings: float = 0.0
        self.cash: float = initial_capital
        self.portfolio_value = self.cash + self.holdings

        self.positions: Dict[Symbol,Position] = {}
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0

    def generate_orders(self, signal: Signal, current_price: Price):
        """ Generate orders from strategy signals

            currently only supports one order for a single symbol
            for simplicity

            signal might want to buy at a certain time but there might be
            a queue of orders to be exectued, keep signal timestamp
            order and Trade timestamp separate
        """


        # percentage holding of all available capital
        current_pct_holding = self.holdings / self.portfolio_value
        # how much the signal wants to allocate to the asset
        needed_pct_holding = signal.strength - current_pct_holding
        needed_holdings_value = self.portfolio_value * needed_pct_holding
        order_qty = int(needed_holdings_value / current_price)
        order_type = OrderType.MARKET  # Only supported currently, can extend later on
        side = TradeSide.BUY if needed_pct_holding > 0 else TradeSide.SELL
        return Order(
            signal.timestamp,
            signal.symbol,
            order_type,
            side,
            order_qty,
            current_price
        )

    def update_positions(self, trade: Optional[Trade]):
        """ Updates positions

           We also calculate correct realised and unrealised PnL from buying and
           selling
        """
        if trade is None:
            return

        sym: Symbol = trade.symbol
        if sym not in self.positions:
            """ Currently can only go long if
                we have no positions we cannot go short
            """
            assert trade.side == TradeSide.BUY

            initial_position: Position = Position(sym)
            initial_position_lot: PositionLot = PositionLot(
                trade.timestamp,
                trade.quantity,
                trade.execution_price
            )
            initial_position.add_position_lot(initial_position_lot)
            self.positions[sym] = initial_position
            logger.info("Updated portfolio.....")
            # TODO: fazeptr update realised/ unrealised pnl here appropriately
            # TODO or split out the logic to do it more nicely
            self.cash -= trade.quantity * trade.execution_price


        else:
            """ Here we can buy or sell now as we have a position"""

            trade_side: TradeSide = trade.side
            if trade_side == TradeSide.BUY:
                lot_to_add: PositionLot = PositionLot(
                    trade.timestamp,
                    trade.quantity,
                    trade.execution_price
                )
                self.positions[sym].add_position_lot(lot_to_add)
                # TODO: fazeptr update realised/ unrealised pnl here appropriately
                # TODO or split out the logic to do it more nicely

                #How much it costs to do this trade
                self.cash -= trade.quantity * trade.execution_price
                logger.info("Updated portfolio.....")
            else:
                realised_pnl_from_trade = self.positions[sym].close_position_lot(trade)

                # TODO: fazeptr update realised/ unrealised pnl here appropriately
                # TODO or split out the logic to do it more nicely, currently
                # TODO: realised pnl goes into cash as well
                #How much it costs to do this trade
                # realised pnl is from closed trades but also affects our cash
                self.realized_pnl += realised_pnl_from_trade
                self.cash += realised_pnl_from_trade

                logger.info("Updated portfolio.....")


    def mark_to_market(self, current_price: Price):
        """ Mark to Market based on current price"""
        self._calculate_unrealised_pnl(current_price)
        self._calculate_holdings(current_price)
        self._calculate_portfolio_value()

    def _calculate_unrealised_pnl(self, current_price: Price):
        """
        Calculates the current Marked to Market unrealised pnl from all open positions

        """
        total_unrealised_pnl = 0.0
        for symbol, position in self.positions.items():
            for position_lot in position.position_lots:
                # qty we hold * current market price - trade_price
                total_unrealised_pnl += position_lot.quantity * (current_price - position_lot.price)
        self.unrealized_pnl = total_unrealised_pnl


    def _calculate_holdings(self, current_price: Price):
        """ Calculates total Marked to market value of all open positions """
        total_holdings = 0.0
        for symbol, position in self.positions.items():
            for position_lot in position.position_lots:
                # qty we hold * current market price - trade_price
                total_holdings += position_lot.quantity * current_price
        self.holdings = total_holdings


    def _calculate_portfolio_value(self):
        self.portfolio_value = self.holdings + self.cash

    def get_unrealised_pnl(self):
        return self.unrealized_pnl


    def get_realised_pnl(self):
        return self.realized_pnl


    def get_portfolio_value(self):
        return self.portfolio_value




