#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from models.dbFundTransactions import fundsTrade



if __name__ == "__main__":
    dbFunds = fundsTrade()
    # dbFunds.add('测试', '123123', '2022-01-01', tradeType.buy,
    #            4521, 10.98, 87.01, 123123.11, 343.11)
    result = dbFunds.getAll()
    for item in result:
        for attr, value in item.__dict__.items():
            print(attr, value)

    del dbFunds
