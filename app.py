#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"


from flask_cors import CORS
from flask import Flask, render_template
from route.stock import stock_api
from route.fundTrade import fundTradeApi
from route.fundHold import fundHoldApi
from cache import cache
from route.auth import auth, generateAuthToken


app = Flask(__name__, static_folder="../../frontend/vue_stock_view/dist/static",
            template_folder="../../frontend/vue_stock_view/dist")


cache.init_app(app)

CORS(app, resources=r'/*')


app.register_blueprint(stock_api)
app.register_blueprint(fundTradeApi)
app.register_blueprint(fundHoldApi)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/tools/clearcache')
@auth.login_required
def clearCache():
    cache.clear()
    return "{'code':200,'msg':'ok'}"


@ app.route('/test/1')
def test1():
    res = generateAuthToken('admin', '123456')
    return res


if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000, debug=True,
            threaded=True)
