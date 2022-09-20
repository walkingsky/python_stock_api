#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response
from models.stockService import StockService

fund_api = Blueprint('fund_api', __name__)


@fund_api.route('/apis/fund/search')
def searchFund():
    # 按照关键字搜索基金
    pass
