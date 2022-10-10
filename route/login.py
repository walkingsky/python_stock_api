#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask import Blueprint
from pre_request import pre, Rule
from flask.helpers import make_response
from route.auth import login

loginApi = Blueprint('loginApi', __name__)


@loginApi.route('/apis/login', methods=['POST'])
def loginroute():
    # 登录
    rule = {
        "username": Rule(type=str, required=True),
        "password": Rule(type=str, required=True),
    }
    try:
        params = pre.parse(rule=rule)
    except:
        return make_response({"error": "参数错误"})
    pass

    username = params['username']
    password = params['password']
    token = login(username, password)
    if token == False:
        return make_response({'code': 401, 'error': '用户名密码错误'})
    else:
        return make_response({'code': 200, 'token': token})
