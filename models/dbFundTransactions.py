#!/usr/bin/env python
# -*- coding:utf-8 -*-

import enum
from sqlalchemy import create_engine, Column, Integer, String, Float
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc


engine = create_engine('sqlite:///fund.db?check_same_thread=False', echo=True)

Base = declarative_base()


class fundTable(Base):
    __tablename__ = "funds"

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
        self.namsharese = shares
        self.nav = nav
        self.commission = commission
        self.amount = amount
        self.returned = returned


Base.metadata.create_all(engine)

# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()


class foudsTrade:
    def add(self, name, code, tradeDate, type, shares, nav, commission, amount, returned):
        # try:
        add_trade = fundTable(name, code, tradeDate, type,
                              shares, nav, commission, amount, returned)
        session.add(add_trade)
        session.commit()
        return True
        # except exc.SQLAlchemyError:
        return False

    def getAll(self):
        try:
            trades = session.query(fundTable).all()
            for item in trades:
                print(item.name)
            return trades
        except exc.SQLAlchemyError:
            return None

    def modifyById(self, id, data={}):
        try:
            session.query(fundTable).filter_by(id=id).update(data)
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delById(self, id):
        try:
            session.query(fundTable).filter_by(id=id).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delAll(self):
        try:
            session.query(fundTable).delete()
            session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def __del__(self):
        session.close()
