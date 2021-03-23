# -*- coding: utf-8 -*-
# @Time    : 7/3/2021 9:50 AM
# @Author  : Joseph Chen
# @Email   : josephchenhk@gmail.com
# @FileName: engine.py
# @Software: PyCharm

from datetime import datetime
from typing import List, Union

from qtrader.core.balance import AccountBalance
from qtrader.core.constants import Direction, Offset, OrderType
from qtrader.core.deal import Deal
from qtrader.core.order import Order
from qtrader.core.portfolio import Portfolio
from qtrader.core.position import PositionData
from qtrader.core.security import Stock
from qtrader.core.data import Bar, _get_full_data
from qtrader.core.logger import logger


class Engine:

    """Execution engine"""

    def __init__(self, portfolio:Portfolio):
        self.portfolio = portfolio
        self.position = portfolio.position
        self.account_balance = portfolio.account_balance
        self.market = portfolio.market
        self.log = logger

    def send_order(self,
        security:Stock,
        price:float,
        quantity:float,
        direction:Direction,
        offset:Offset,
        order_type:OrderType
        )->str:
        """发出订单"""
        create_time = self.market.market_datetime
        order = Order(
            security = security,
            price = price,
            quantity = quantity,
            direction = direction,
            offset = offset,
            order_type = order_type,
            create_time = create_time
        )
        orderid = self.market.place_order(order)
        return orderid

    def cancel_order(self, orderid):
        """取消订单"""
        self.market.cancel_order(orderid)

    def get_order(self, orderid):
        """获取订单的状态"""
        return self.market.get_order(orderid)

    def get_recent_bar(self,
                       security:Stock,
                       cur_datetime:datetime=datetime.now(),
                       num_of_bars:int=1
        )->Union[Bar, List[Bar]]:
        """
        获取最接近当前时间的数据点 (或者最近一段bar数据)
        """
        return self.market.get_recent_bar(security, cur_datetime, num_of_bars)

    def get_history_bar(self,
                        security: Stock,
                        start: datetime,
                        end: datetime
        )->List[Bar]:
        """
        获取历史时间段的bar数据
        """
        df = _get_full_data(security=security, start=start, end=end)
        bars = []
        for _, row in df.iterrows():
            bar_time = datetime.strptime(row["time_key"], "%Y-%m-%d %H:%M:%S")
            bar = Bar(
                datetime=bar_time,
                security=security,
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"]
            )
            bars.append(bar)
        return bars

    def find_deals_with_orderid(self, orderid:str)->List[Deal]:
        """根据orderid找出成交的deal"""
        return self.market.find_deals_with_orderid(orderid)

    def get_balance(self)->AccountBalance:
        """balance"""
        return self.portfolio.account_balance

    def get_broker_balance(self)->AccountBalance:
        """broker balance"""
        return self.market.get_broker_balance()

    def get_position(self, security:Stock, direction:Direction)->PositionData:
        """position"""
        return self.portfolio.position.get_position(security, direction)

    def get_broker_position(self, security:Stock, direction:Direction)->PositionData:
        """broker position"""
        return self.market.get_broker_position(security, direction)

    def get_all_positions(self)->List[PositionData]:
        """all positions"""
        return self.portfolio.position.get_all_positions()

    def get_all_broker_positions(self)->List[PositionData]:
        """all broker positions"""
        return self.market.get_all_broker_positions()
