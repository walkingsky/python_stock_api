#!/usr/bin/env python
# -*- coding:utf-8 -*-

import enum
from sqlalchemy import create_engine, Column, Integer, String, Float
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import pandas as pd


engine = create_engine('sqlite:///fund.db?check_same_thread=False', echo=False)

Base = declarative_base()


class fundsTradeTable(Base):
    # 基金交易记录表
    __tablename__ = "fundstrade"

    id = Column(Integer, primary_key=True)
    # 基金名称
    name = Column(String(40))
    # 基金代码
    code = Column(String(6))
    # 交易日期
    tradedate = Column(String(10))
    # 交易类型（买卖方向）
    type = Column(String(4))
    # 份额
    shares = Column(Integer)
    # 单位净值
    nav = Column(Float(precision=2))
    # 手续费
    commission = Column(Float(precision=2), default=0)
    # 交易金额
    amount = Column(Float(precision=2))
    # 转出退回金额
    returned = Column(Float(precision=2), default=0)

    def __init__(self, name, code, tradeDate, type, shares, nav, commission, amount, returned):
        self.name = name
        self.code = code
        self.tradedate = tradeDate
        self.type = type
        self.shares = shares
        self.nav = nav
        self.commission = commission
        self.amount = amount
        self.returned = returned


class fundsHoldTable(Base):
    # 基金持仓记录表
    __tablename__ = "fundshold"

    id = Column(Integer, primary_key=True)
    # 基金名称
    name = Column(String(40))
    # 基金代码
    code = Column(String(6))

    # 份额
    shares = Column(Integer)
    # 持仓成本价
    costprice = Column(Float(precision=2))

    def __init__(self, name, code, shares, costprice):
        self.name = name
        self.code = code
        self.shares = shares
        self.costprice = costprice


Base.metadata.create_all(engine)

# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()


class fundsTrade:
    # 基金交易记录类
    def add(self, name, code, tradeDate, type, shares, nav, commission, amount, returned):
        try:
            add_trade = fundsTradeTable(name, code, tradeDate, type,
                                        shares, nav, commission, amount, returned)
            session.add(add_trade)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getAll(self):
        try:
            trades = session.query(fundsTradeTable).all()
            return trades
        except exc.SQLAlchemyError:
            return None

    def modifyById(self, id, data={}):
        try:
            session.query(fundsTradeTable).filter_by(id=id).update(data)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delById(self, id):
        try:
            session.query(fundsTradeTable).filter_by(id=id).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getByCode(self, code):
        try:
            trades = session.query(fundsTradeTable).filter_by(code=code).all()
            return trades
        except exc.SQLAlchemyError:
            return None

    def delAll(self):
        try:
            session.query(fundsTradeTable).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getById(self, id):
        try:
            trade = session.query(fundsTradeTable).filter_by(id=id).first()
            session.commit()
            return trade
        except exc.SQLAlchemyError:
            return False

    def __del__(self):
        session.close()

    def pandasRead(self):
        return pd.read_sql('fundstrade', engine)


class fundsHold:
    # 基金持仓记录类
    def add(self, name, code,  shares, costprice):
        try:
            add_trade = fundsHoldTable(name, code, shares, costprice)
            session.add(add_trade)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delByCode(self, code):
        try:
            session.query(fundsHoldTable).filter_by(code=code).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def modifyBycode(self, code, data={}):
        try:
            session.query(fundsHoldTable).filter_by(code=code).update(data)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def getAll(self):
        try:
            trades = session.query(fundsHoldTable).all()
            return trades
        except exc.SQLAlchemyError:
            return None

    def delAll(self):
        try:
            session.query(fundsHoldTable).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def __del__(self):
        session.close()

    def pandasRead(self):
        return pd.read_sql('fundsHold', engine)
