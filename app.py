#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from ast import Try
from hashlib import new
from flask_cors import CORS
# , render_template, Response, redirect, url_for
from flask import Flask, request, jsonify
from pre_request import pre, Rule
from flask.helpers import make_response
from models.stockService import StockService

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/apis/test/')
def api_test():
    ans = jsonify({
        "product": [5, 20, 36, 10, 10, 20]
    })
    return make_response(ans)


@app.route('/apis/stock/hold')
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


@app.route('/apis/stock/historydata')
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


@app.route('/apis/stock/history')
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


@app.route('/apis/stock')
def getStockByCode():
    # 获取股票最后一天的行情数据
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
    data = stockService.getStockByCode(code)
    # print(data)
    return make_response(data)


@app.route('/apis/industry')
def getIndustryData():
    # 获取行业排行数据
    rule = {
        "kind": Rule(type=str, required=True, enum=['fluctuate', 'capital']),
        "sort": Rule(type=str, required=True, enum=['asc', 'desc'])
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    data = stockService.getIndustryData(params['kind'], params['sort'])
    # print(data)
    return make_response(data)


@app.route('/apis/industry/info')
def getIndustryInfoData():
    # 获取行业内排行数据
    rule = {
        "kind": Rule(type=str, required=True, enum=['fluctuate', 'capital']),
        "sort": Rule(type=str, required=True, enum=['asc', 'desc']),
        "industryCode": Rule(type=str, required=True, reg=r'[\da-zA-Z]{6}')
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})

    stockService = StockService()
    data = stockService.getIndustryInfoData(
        params['industryCode'], params['kind'], params['sort'])
    # print(data)
    return make_response(data)


if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000, debug=True,
            threaded=True)
