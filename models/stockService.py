#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import os
import glob
import time
import re
import pandas as pd
import requests


class StockService:

    def getPath(self):
        if os.path.exists('/data'):
            path = "/data/tools/python/stock_csv"
        else:
            path = "F:/study/python/stock_csv"
        return path

    def getHold(self):
        '''
        从单一的一个csv文件，获取股票的持仓数据
        '''
        path = self.getPath()
        df = pd.read_csv(path+'/广发操盘手-持仓.csv', sep=',',
                         dtype={'证券代码': str, '股东账号': str})
        # 合并相同股票
        df['证券代码'] = df['证券代码'].str.strip()
        result_df = df.reset_index(drop=True)

        response_body = '{"code":200,"results":['
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            response_body = response_body + '{"key":'+str(index)+',"code":"'+row['证券代码']+'","name":"'\
                + row['证券名称']+'","num":"'+str(row['当前数量'])+'","costPrice":' + \
                str(row['成本价'])+',"marketVule":'+str(row['市值价']) + \
                ',"market":"'+row['市场']+'"}'
            if index < row_num - 1:
                response_body = response_body + ','
        response_body = response_body + ']}'
        print(response_body)
        return response_body

    def getHistoryHold(self):
        '''
        从csv文件中，获取所有持仓过的股票数据
        '''
        path = self.getPath()
        all_files = glob.glob(os.path.join(path, "*今日成交.*.csv"))
        if not all_files:
            return '{}'

        all_df = []
        for f in all_files:
            df = pd.read_csv(f, sep=',', usecols=[
                             '市场', '证券代码', '证券名称'], dtype={'证券代码': str})
            all_df.append(df)

        merged_df = pd.concat(all_df, ignore_index=True, sort=True).drop_duplicates(
            subset=['市场', '证券代码']).reset_index(drop=True)
        # print(merged_df)
        merged_df['证券代码'] = merged_df['证券代码'].str.strip()
        row_num = merged_df.shape[0]
        json_str = '{"code":200,"results":['
        for index, row in merged_df.iterrows():
            json_str = json_str + '{"key":'+str(index)+',"code":"'+row['证券代码']+'","name":"'\
                + row['证券名称'] + '","market":"'+row['市场']+'"}'
            if index < row_num - 1:
                json_str = json_str + ','

        json_str = json_str + ']}'
        # print(json_str)
        return json_str

    def getHistory(self, stock_code, market):
        '''
        通过股票代码，市场，从csv列表文件中获取股票的历史交易数据
        '''
        path = self.getPath()
        all_files = glob.glob(os.path.join(path, "*今日成交.*.csv"))
        if not all_files:
            return '{}'

        # print(all_files)
        # return
        all_df = []
        for f in all_files:
            df = pd.read_csv(f, sep=',', dtype={'证券代码': str, '股东账号': str})
            file_name = f.split('/')[-1]
            date = file_name.split('.')
            YEARS = re.findall(r'\d{4}', date[1])
            if len(YEARS) == 0:
                os.stat(f).st_mtime
                Y = time.strftime("%Y", time.localtime(os.stat(f).st_mtime))
                df['成交日期'] = Y + '-' + date[1]+'-'+date[2]
            else:
                Y = YEARS[0]
                df['成交日期'] = Y + '-' + date[2]+'-'+date[3]
            # print(Y)

            all_df.append(df)

        merged_df = pd.concat(all_df, ignore_index=True, sort=True)
        merged_df['证券代码'] = merged_df['证券代码'].str.strip()
        result_df = merged_df[(merged_df['市场'] == market) & (
            merged_df['证券代码'] == stock_code)].reset_index(drop=True)
        # print(result_df)
        response_body = '{"code":200,"results":['
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            response_body = response_body + '{"code":"'+stock_code+'","date":"'\
                + row['成交日期']+'","time":"'+row['成交时间'].strip()+'","sell_buy":"'+row['买卖方向']+'","price":' + \
                str(row['成交价格'])+',"num":'+str(row['成交数量'])+'}'
            if index < row_num - 1:
                response_body = response_body + ','
        response_body = response_body + ']}'
        return response_body

    def getStockByCode(self, code):
        '''
            获取股票的是实时信息
            #code 参数，code 可以是一个，也可以是用逗号分隔的多个。 要带上市场简写，比如 sh600036,sz300301
        '''
        base_url = 'http://img1.money.126.net/data/hs/time/today/'+code+'.json'
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result
