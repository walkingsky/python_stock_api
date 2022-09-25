#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'filesystem',
                      'CACHE_DIR': './temp_data/cache',  # 缓存目录
                      'CACHE_DEFAULT_TIMEOUT': 600,
                      'CACHE_THRESHOLD': 200})
