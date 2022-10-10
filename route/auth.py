#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired, BadData
from flask import make_response, jsonify, g

SECRET_KEY = 'xa*%On^HqUvxh2Dwra#(RR$oBF$pD~M%'
USERNAME = 'admin'
PASSWORD = '123456'

auth = HTTPTokenAuth(scheme='bearer')


@auth.verify_token
def verifyToken(token):

    g.token_error = False
    g.token_timeout = False
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
        userName = data['userName']
        password = data['password']
    except SignatureExpired:
        g.token_timeout = True
        # return make_response(jsonify({'code': 402, 'msg': 'token不正确'}), 402)
        return False
    except BadSignature:
        g.token_error = True
        # return make_response(jsonify({'code': 401, 'msg': 'token过期'}), 401)
        return False
    userName = data['userName']
    password = data['password']
    return userName == USERNAME and password == PASSWORD


@auth.error_handler
def unauthorized():
    if g.token_timeout:
        return make_response(jsonify({'code': 401, 'msg': 'token过期'}), 401)
    if g.token_error:
        return make_response(jsonify({'code': 402, 'msg': 'token不正确'}), 401)

    return make_response(jsonify({'code': 500, 'msg': '认证不正确'}), 401)


def login(username, password):
    if username == USERNAME and password == PASSWORD:
        return generateAuthToken(username, password)
    else:
        return False


def generateAuthToken(userName, password):
    s = Serializer(SECRET_KEY, expires_in=24*3600*7)
    return s.dumps({'userName': userName, 'password': password}).decode()
