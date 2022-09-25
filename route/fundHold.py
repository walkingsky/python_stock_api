#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response
from models.dbFund import fundsHold
from models.fundService import FundService

fundHoldApi = Blueprint('fundHoldApi', __name__)


@fundHoldApi.route('/apis/fund/hold/getall')
def getAllTradeRecord():
    # 获取所有的基金持仓记录
    fundsHoldDb = fundsHold()
    data = fundsHoldDb.getAll()

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

    del fundsHoldDb
    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/get')
def getById():
    # 按照id获取基金持仓
    rule = {
        "id": Rule(type=int, required=True, gte=1),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsHoldDb = fundsHold()
    data = fundsHoldDb.getById(id=params['id'])
    res = {}
    if(data != None):
        res['code'] = 200
        res['data'] = data
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False
    del fundsHoldDb
    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/gz')
def getFundGz():
    # 获取基金的估值列表
    rule = {
        "codes": Rule(type=str, required=True, reg=r'[\d,]+'),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    codes = params['codes'].split(',')
    fundService = FundService()
    res = {}
    data = []
    for code in codes:
        results = fundService.getFundgz(code)
        data.append(results)

    res['code'] = 200
    res['data'] = data
    res['success'] = True

    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/lsjz')
def getFundLsjz():
    # 获取基金的估值列表
    rule = {
        "code": Rule(type=str, required=True, reg=r'\d{6}'),
        "size": Rule(type=int, required=True, default=50, gte=50, lte=300),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    code = params['code']
    size = params['size']
    fundService = FundService()
    data = fundService.getFundHistory(code=code, size=size)
    return make_response(data)
