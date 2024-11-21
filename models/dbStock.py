#!/usr/bin/env python
# -*- coding:utf-8 -*-

import enum
from sqlalchemy import create_engine, Column, Integer, String, Float
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import pandas as pd


engine = create_engine('sqlite:///stock.db?check_same_thread=False', echo=False)

Base = declarative_base()


class stockTradeTable(Base):
    # 股票交易记录表
    __tablename__ = "stocktrade"

    id = Column(Integer, primary_key=True)
    # 股票名称
    name = Column(String(40))
    # 股票代码
    code = Column(String(6))
    # 交易日期
    tradedate = Column(String(10))
    # 交易类型（买卖方向）
    type = Column(String(4))
    # 成交数量
    shares = Column(Integer)
    # 成交价格
    nav = Column(Float(precision=2))
    # 手续费
    commission = Column(Float(precision=2), default=0)
    # 交易金额
    amount = Column(Float(precision=2))
    

    def __init__(self, name, code, tradeDate, type, shares, nav, commission, amount):
        self.name = name
        self.code = code
        self.tradedate = tradeDate
        self.type = type
        self.shares = shares
        self.nav = nav
        self.commission = commission
        self.amount = amount


Base.metadata.create_all(engine)

# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()


class stockTrade:
    # 股票交易记录类
    def add(self, name, code, tradeDate, type, shares, nav, commission, amount):
        try:
            add_trade = stockTradeTable(name, code, tradeDate, type,
                                        shares, nav, commission, amount)
            session.add(add_trade)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getAll(self):
        try:
            trades = session.query(stockTradeTable).all()
            return trades
        except exc.SQLAlchemyError:
            return None

    def modifyById(self, id, data={}):
        try:
            session.query(stockTradeTable).filter_by(id=id).update(data)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delById(self, id):
        try:
            session.query(stockTradeTable).filter_by(id=id).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getByCode(self, code):
        try:
            trades = session.query(stockTradeTable).filter_by(code=code).all()
            return trades
        except exc.SQLAlchemyError:
            return None

    def delAll(self):
        try:
            session.query(stockTradeTable).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getById(self, id):
        try:
            trade = session.query(stockTradeTable).filter_by(id=id).first()
            session.commit()
            return trade
        except exc.SQLAlchemyError:
            return False

    def __del__(self):
        session.close()

    def pandasRead(self):
        return pd.read_sql('stocktrade', engine)


