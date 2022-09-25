#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import json
import requests

# 保留？还是舍弃？


class FundService:

    def getFundSeggestByKey(self, key):
        '''
            通过关键字搜索基金，返回基金列表
        '''
        #base_url = 'https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=0&key='+key
        base_url = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=0&key=' + key
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return json.loads(res.text)['Datas']['FundList']
        return result

    def getFundHistory(self, code, size=50):
        '''
            获取基金的历史净值
        '''
        headers = {'Referer': 'http://fundf10.eastmoney.com/'}
        base_url = 'http://api.fund.eastmoney.com/f10/lsjz?fundCode=' + \
            code+'&pageIndex=1&pageSize=' + str(size)
        res = requests.get(base_url, headers=headers)
        result = {}
        if(res.status_code == 200):
            return json.loads(res.text)
        return result

    def getFundgz(self, code):
        '''
            获取基金的实时估值
        '''
        base_url = 'http://fundgz.1234567.com.cn/js/'+code+'.js'
        res = requests.get(base_url)

        text = res.text[8:-2]
        if len(text) < 3:
            text = '{"fundcode":"'+code+'","gsz":"--","gszzl":"--"}'
        return json.loads(text)
