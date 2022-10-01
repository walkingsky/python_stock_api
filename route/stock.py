#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint, current_app, request
from pre_request import pre, Rule
from flask.helpers import make_response
from models.stockService import StockService
from cache import cache

stock_api = Blueprint('stock_api', __name__)

# 行业数量默认限制
limitIn = 5
# 行业内股票数量默认限制
limitStock = 10


def key_prefix_func():
    key_prefix = "%s"
    with current_app.app_context():
        if '%s' in key_prefix:
            # 这里改成request.url
            cache_key = key_prefix % request.url
        else:
            cache_key = key_prefix
    return cache_key


@stock_api.route('/apis/stock/hold')
@cache.cached(timeout=600, key_prefix=key_prefix_func)
def getStockHold():
    # 获取持有股票信息
    rule = {
        "history": Rule(type=str, required=False, default='0', enum=['1', '0']),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    if params['history'] == '0':
        stocks = stockService.getHold()
    else:
        stocks = stockService.getHistoryHold()
    return make_response(stocks)


@stock_api.route('/apis/stock/historydata')
def getStockHistoryData():
    # 获取股票历史行情
    rule = {
        "market": Rule(type=str, required=True, enum=['上海', '深圳', '北京']),
        "code": Rule(type=str, required=True, reg=r'\d{6}')
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    code = params['code']
    if params['market'] == '上海':
        code = '1.' + params['code']
    if params['market'] == '深圳':
        code = '0.' + params['code']
    if params['market'] == '北京':
        code = '2.' + params['code']

    stockService = StockService()
    data = stockService.getStockHistoryData(code)
    # print(data)
    return make_response(data)


@stock_api.route('/apis/stock/history')
def getStorkHistory():
    # 获取股票历史交易数据
    rule = {
        "market": Rule(type=str, required=True, enum=['上海', '深圳', '北京']),
        "code": Rule(type=str, required=True, reg=r'\d{6}')
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    history = stockService.getHistory(params['code'], params['market'])
    return make_response(history)


@stock_api.route('/apis/stock/126')
def getStockByCode126():
    # 获取股票最后一天的行情数据,126 的行情数据
    rule = {
        "market": Rule(type=str, required=True, enum=['上海', '深圳', '北京']),
        "code": Rule(type=str, required=True, reg=r'\d{6}')
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    code = params['code']
    if params['market'] == '上海':
        code = '0' + params['code']
    if params['market'] == '深圳':
        code = '1' + params['code']
    if params['market'] == '北京':
        code = '2' + params['code']

    stockService = StockService()
    data = stockService.getStockByCode126(code)
    # print(data)
    return make_response(data)


@stock_api.route('/apis/stock/east')
def getStockByCodeEast():
    # 获取股票最后一天的行情数据,东财的行情数据
    rule = {
        "market": Rule(type=str, required=True, enum=['上海', '深圳', '北京']),
        "code": Rule(type=str, required=True, reg=r'\d{6}')
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    code = params['code']
    if params['market'] == '上海':
        code = '1.' + params['code']
    if params['market'] == '深圳':
        code = '0.' + params['code']
    if params['market'] == '北京':
        code = '2.' + params['code']

    stockService = StockService()
    data = stockService.getStockByCodeEastM(code)
    # print(data)
    return make_response(data)


@stock_api.route('/apis/industry')
def getIndustryData():
    # 获取行业排行数据
    rule = {
        "kind": Rule(type=str, required=True, enum=['fluctuate', 'capital']),
        "sort": Rule(type=str, required=True, enum=['asc', 'desc']),
        "pz": Rule(type=int, required=False, default=limitIn, gte=5, lte=100),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    data = stockService.getIndustryData(
        params['kind'], params['sort'], params['pz'])
    # print(data)
    return make_response(data)


@stock_api.route('/apis/industry/info')
def getIndustryInfoData():
    # 获取行业内排行数据
    rule = {
        "kind": Rule(type=str, required=True, enum=['fluctuate', 'capital']),
        "sort": Rule(type=str, required=True, enum=['asc', 'desc']),
        "industryCode": Rule(type=str, required=True, reg=r'[\da-zA-Z]{6}'),
        # "pz": Rule(type=int, required=False, default=limitStock, gte=10, lte=1000),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    data = stockService.getIndustryInfoData(
        params['industryCode'], params['kind'], params['sort'], limitStock)
    # print(data)
    return make_response(data)


@stock_api.route('/apis/industry/history')
def getIndustryHistoryData():
    # 获取行业内排行数据
    rule = {
        "industryCode": Rule(type=str, required=True, reg=r'[\da-zA-Z]{6}'),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    data = stockService.getIndustryHistoryData(
        params['industryCode'])
    # print(data)
    return make_response(data)
