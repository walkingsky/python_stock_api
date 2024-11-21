#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"


from flask_cors import CORS
from flask import Flask, render_template
from route.stock import stock_api
from route.fundTrade import fundTradeApi
from route.fundHold import fundHoldApi
from route.login import loginApi
from cache import cache
from route.auth import auth
from route.longConnect import longConnect

from config import WEB_STATIC_DIR,WEB_DIR,HOST,PORT,IS_DEBUG


app = Flask(__name__, static_folder=WEB_STATIC_DIR,
            template_folder=WEB_DIR)


cache.init_app(app)

CORS(app, resources=r'/*')


app.register_blueprint(stock_api)
app.register_blueprint(fundTradeApi)
app.register_blueprint(fundHoldApi)
app.register_blueprint(loginApi)
app.register_blueprint(longConnect)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/tools/clearcache')
@auth.login_required
def clearCache():
    cache.clear()
    return "{'code':200,'msg':'ok'}"


if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host=HOST, port=PORT, debug=IS_DEBUG,
            threaded=True)
    # http_serve = WSGIServer((HOST,PORT),app)
    # http_serve.serve_forever()
