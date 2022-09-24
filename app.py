#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"


from flask_cors import CORS
from flask import Flask, render_template
from route.stock import stock_api
from route.fund import fund_api
from flask_cache import Cache


app = Flask(__name__, static_folder="../../frontend/vue_stock_view/dist/static",
            template_folder="../../frontend/vue_stock_view/dist")

cache = Cache(app, config={'CACHE_TYPE': 'filesystem',
                           'CACHE_DIR': './temp_data/cache',  # 缓存目录
                           'CACHE_DEFAULT_TIMEOUT': 600,
                           'CACHE_THRESHOLD': 200})

CORS(app, resources=r'/*')

app.register_blueprint(stock_api)
app.register_blueprint(fund_api)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000, debug=True,
            threaded=True)
