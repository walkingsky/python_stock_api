#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response, request
from models.fundService import FundService
from models.dbFundTransactions import foudsTrade
import json

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
    data = {'Datas': data}
    # print(data)
    # return make_response(','.join(data))
    return json.dumps(data)


@fund_api.route('/apis/fund/add', methods=['POST'])
def addTradeRecord():
    # 添加基金交易记录
    print(request.get_json())
    rule = {
        "name": Rule(type=str, required=True),
        "code": Rule(type=str, required=True, reg=r'[a-zA-Z\d]{6}'),
        "tradeDate": Rule(type=str, required=True, reg=r'\d{4}-\d{2}-\d{2}'),
        "type": Rule(type=str, required=True, enum=['买入', '卖出', '转入', '转出']),
        "shares": Rule(type=int, required=True, gte=1),
        "nav": Rule(type=float, required=True, gte=0),
        "commission": Rule(type=float, required=False),
        "amount": Rule(type=float, required=True, gte=1),
        "returned": Rule(type=float, required=False),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    foudsTradeDb = foudsTrade()
    data = foudsTradeDb.add(
        name=params['name'], code=params['code'], tradeDate=params['tradeDate'],
        type=params['type'], shares=params['shares'], nav=params['nav'], commission=params['commission'],
        amount=params['amount'], returned=params['returned'])
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del foudsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/getall')
def getAllTradeRecord():
    # 获取所有的基金交易记录
    foudsTradeDb = foudsTrade()
    data = foudsTradeDb.getAll()
    res = {}
    if(data != None):
        res['data'] = data
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del foudsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/modify')
def modidyTradeRecord():
    # 获取所有的基金交易记录
    rule = {
        "id": Rule(type=int, required=True),
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

    foudsTradeDb = foudsTrade()
    data = foudsTradeDb.modifyById(id=params['id'],
                                   data={'name': params['name'], 'code': params['code'], 'tradeDate': params['tradeDate'],
                                   'type': params['type'], 'shares': params['shares'], 'nav': params['nav'], 'commission': params['commission'],
                                         'amount': params['amount'], 'returned': params['returned']})
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del foudsTradeDb
    return make_response(res)
