#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import json
import requests
from models.dbFundTransactions import fundsTrade


class FundService:
    def __init__(self) -> None:
        self.dbFunds = fundsTrade()

    def getFundSeggestByKey(self, key):
        '''
            通过关键字搜索基金，返回基金列表
        '''
        #base_url = 'https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=0&key='+key
        base_url = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=0&key=' + key
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return json.loads(res.text)['Datas']['FundList']
        return result

    def addTradeRecord(self, name, code, tradeDate, type, shares, nav, commission, amount, returned):
        #dbFunds = fundsTrade()
        return self.dbFunds.add(name, code, tradeDate, type, shares, nav, commission, amount, returned)

    def getAllTradeRecord(self):
        return self.dbFunds.getAll()

    def __del__(self):
        del self.dbFunds
