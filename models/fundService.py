#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import os
import glob
import time
import pandas as pd
import requests
import numpy as np
from models.dbFundTransactions import foudsTrade, tradeType


class FundService:
    def __init__(self) -> None:
        self.dbFunds = foudsTrade()

    def getFundSeggestByKey(self, key):
        '''
            通过关键字搜索基金，返回基金列表
        '''
        base_url = 'https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=0&key='+key
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def addTradeRecord(self, name, code, tradeDate, type, shares, nav, commission, amount, returned):
        #dbFunds = foudsTrade()
        return self.dbFunds.add(name, code, tradeDate, type, shares, nav, commission, amount, returned)

    def getAllTradeRecord(self):
        return self.dbFunds.getAll()

    def __del__(self):
        del self.dbFunds
