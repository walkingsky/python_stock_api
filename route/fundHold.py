#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response
from models.dbFund import fundsHold
from models.fundService import FundService
from route.auth import auth

fundHoldApi = Blueprint('fundHoldApi', __name__)


@fundHoldApi.route('/apis/fund/hold/add', methods=['POST'])
@auth.login_required
def addHoldRecord():
    # 添加基金持仓
    rule = {
        "name": Rule(type=str, required=True),
        "code": Rule(type=str, required=True, reg=r'[a-zA-Z\d]{6}'),
        "shares": Rule(type=float, required=True, gte=1),
        "costprice": Rule(type=float, required=True, gte=0),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsHoldDb = fundsHold()
    data = fundsHoldDb.add(
        name=params['name'], code=params['code'],  shares=params['shares'], costprice=params['costprice'])
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del fundsHoldDb
    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/modify', methods=['PUT'])
@auth.login_required
def modidyHoldRecord():
    # 修改记录
    rule = {
        "name": Rule(type=str, required=True),
        "code": Rule(type=str, required=True, reg=r'[a-zA-Z\d]{6}'),
        "shares": Rule(type=float, required=True, gte=1),
        "costprice": Rule(type=float, required=True, gte=0),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsHoldDb = fundsHold()
    data = fundsHoldDb.modifyBycode(code=params['code'],
                                    data={'name': params['name'],   'shares': params['shares'], 'nacostpricev': params['costprice']})
    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False

    del fundsHoldDb
    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/del', methods=['DELETE'])
@auth.login_required
def delByCode():
    # 按照code单条删除记录
    rule = {
        "code": Rule(type=str, required=True, reg=r'[\d,]+'),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    fundsHoldDb = fundsHold()
    data = fundsHoldDb.delByCode(code=params['code'])

    res = {}
    if(data == True):
        res['code'] = 200
        res['success'] = True
    else:
        res['code'] = 201
        res['success'] = False
    del fundsHoldDb
    return make_response(res)


@fundHoldApi.route('/apis/fund/hold/getall')
@auth.login_required
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
@auth.login_required
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
@auth.login_required
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
@auth.login_required
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
