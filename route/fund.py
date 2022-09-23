#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response, request
from models.fundService import FundService
from models.dbFundTransactions import fundsTrade
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
        "tradedate": Rule(type=str, required=True, reg=r'\d{4}-\d{2}-\d{2}'),
        "type": Rule(type=str, required=True, enum=['买入', '卖出', '转入', '转出', '分红', '增强']),
        "shares": Rule(type=float, required=True, gte=1),
        "nav": Rule(type=float, required=True, gte=0),
        "commission": Rule(type=float, required=False),
        "amount": Rule(type=float, required=True, gte=1),
        "returned": Rule(type=float, required=False),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsTradeDb = fundsTrade()
    data = fundsTradeDb.add(
        name=params['name'], code=params['code'], tradeDate=params['tradedate'],
        type=params['type'], shares=params['shares'], nav=params['nav'], commission=params['commission'],
        amount=params['amount'], returned=params['returned'])
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del fundsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/getall')
def getAllTradeRecord():
    # 获取所有的基金交易记录
    fundsTradeDb = fundsTrade()
    data = fundsTradeDb.getAll()

    res = {}
    if(data != None):
        _data = []
        for item in data:
            items = {}
            for attr, value in item.__dict__.items():
                if attr != '_sa_instance_state':
                    items[attr] = value
            _data.append(items)
        res['data'] = _data
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del fundsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/modify', methods=['PUT'])
def modidyTradeRecord():
    # 获取所有的基金交易记录
    rule = {
        "id": Rule(type=int, required=True),
        "name": Rule(type=str, required=True),
        "code": Rule(type=str, required=True, reg=r'[a-zA-Z\d]{6}'),
        "tradedate": Rule(type=str, required=True, reg=r'\d{4}-\d{2}-\d{2}'),
        "type": Rule(type=str, required=True, enum=['买入', '卖出', '转入', '转出']),
        "shares": Rule(type=float, required=True, gte=1),
        "nav": Rule(type=float, required=True, gte=0),
        "commission": Rule(type=float, required=False),
        "amount": Rule(type=float, required=True, gte=1),
        "returned": Rule(type=float, required=False),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsTradeDb = fundsTrade()
    data = fundsTradeDb.modifyById(id=params['id'],
                                   data={'name': params['name'], 'code': params['code'], 'tradedate': params['tradedate'],
                                   'type': params['type'], 'shares': params['shares'], 'nav': params['nav'], 'commission': params['commission'],
                                         'amount': params['amount'], 'returned': params['returned']})
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del fundsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/get')
def getById():
    # 按照id获取交易记录数据
    rule = {
        "id": Rule(type=int, required=True, gte=1),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsTradeDb = fundsTrade()
    data = fundsTradeDb.getById(id=params['id'])
    res = {}
    if(data != None):
        res['code'] = 200
        res['data'] = data
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False
    del fundsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/del', methods=['DELETE'])
def delById():
    # 按照id 单条删除记录
    rule = {
        "id": Rule(type=int, required=True, gte=1),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsTradeDb = fundsTrade()
    data = fundsTradeDb.delById(id=params['id'])
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False
    del fundsTradeDb
    return make_response(res)


@fund_api.route('/apis/fund/import')
def importCsv():
    # 测试接口，导入服务器本地的一个csv数据文件到数据库

    rule = {
        "csv": Rule(type=int, required=True, gte=1),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsTradeDb = fundsTrade()
    fundsTradeDb.delAll()
    fo = open("./temp_data/基金交易记录完整版.csv", "r", encoding="utf-8")
    lines = fo.readlines()

    for line in lines:
        if lines.index(line) == 0:
            continue
        params = line.split(',')
        data = fundsTradeDb.add(
            name=params[0], code=params[1], tradeDate=params[2], type=params[3],
            shares=params[4], nav=params[5], commission=params[7], amount=params[6],
            returned=params[8])
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False
    del fundsTradeDb
    return make_response(res)
