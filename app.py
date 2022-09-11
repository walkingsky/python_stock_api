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
    stockService = StockService()
    stocks = stockService.getHold()
    return make_response(stocks)


@app.route('/apis/stock/history')
def getStorkHistory():
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


if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000, debug=True)
