#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response
from models.fundService import FundService

fund_api = Blueprint('fund_api', __name__)


@fund_api.route('/apis/fund/search')
def searchFund():
    # 按照关键字搜索基金
    # 获取股票历史行情
    rule = {
        "key": Rule(type=str, required=True)
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})
    pass

    key = params['key']
    fundService = FundService()
    data = fundService.getFundSeggestByKey(key)
    return make_response(data)


@fund_api.route('/apis/fund/add', methods=['POST'])
def addTradeRecord():
    # 添加基金交易记录
    rule = {
        "name": Rule(type=str, required=True),
        "code": Rule(type=str, required=True, reg=r'[a-zA-Z\d]{6}'),
        "tradeDate": Rule(type=str, required=True, reg=r'\d{4}-\d{2}-\d{2}'),
        "type": Rule(type=str, required=True, enum=[1, 2, 3, 4]),
        "shares": Rule(type=int, required=True, gte=1),
        "nav": Rule(type=str, required=True, reg=r'[\d\.]+'),
        "commission": Rule(type=str, required=False, reg=r'[\d\.]+'),
        "amount": Rule(type=str, required=True, reg=r'[\d\.]+'),
        "returned": Rule(type=str, required=False, reg=r'[\d\.]+'),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})
    pass
    fundService = FundService()
    data = fundService.addTradeRecord(
        name=params['name'], code=params['code'], tradeDate=params['tradeDate'],
        type=params['type'], shares=params['shares'], nav=params['nav'], commission=params['commission'],
        amount=params['amount'], returned=params['returned'])
    res = {}
    if(data == True):
        res.code = 200
        res.success = True
    else:
        res.code = 201
        res.success = False

    del fundService
    return make_response(res)


@fund_api.route('/apis/fund/getall')
def getAllTradeRecord():
    fundService = FundService()
    data = fundService.getAllTradeRecord()
    res = {}
    if(data != None):
        res.data = data
        res.code = 200
        res.success = True
    else:
        res.code = 201
        res.success = False

    del fundService
    return make_response(res)
