#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import os
import glob
import time
import re
import pandas as pd


class StockService:

    def getPath(self):
        if os.path.exists('/data'):
            path = "/data/tools/python/stock_csv"
        else:
            path = "F:/study/python/stock_csv"
        return path

    def getHold(self):
        path = self.getPath()
        df = pd.read_csv(path+'/广发操盘手-持仓.csv', sep=',',
                         dtype={'证券代码': str, '股东账号': str})
        # 合并相同股票
        df['证券代码'] = df['证券代码'].str.strip()
        result_df = df.reset_index(drop=True)

        response_body = '{"results":['
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            response_body = response_body + '{"code":"'+row['证券代码']+'","name":"'\
                + row['证券名称']+'","num":"'+str(row['当前数量'])+'","costPrice":' + \
                str(row['成本价'])+',"marketVule":'+str(row['市值价']) + \
                ',"market":"'+row['市场']+'"}'
            if index < row_num - 1:
                response_body = response_body + ','
        response_body = response_body + ']}'
        print(response_body)
        return response_body

    def getHistory(self, stock_code, market):
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
        response_body = '{"history":{'
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            response_body = response_body + '"' + str(index) + '":{"code":"'+stock_code+'","date":"'\
                + row['成交日期']+'","sell_buy":"'+row['买卖方向']+'","price":' + \
                str(row['成交价格'])+',"num":'+str(row['成交数量'])+'}'
            if index < row_num - 1:
                response_body = response_body + ','
        response_body = response_body + '},"position":{'

        all_files = glob.glob(os.path.join(path, "广发操盘手-持仓.*.csv"))
        if not all_files:
            response_body = response_body + '}'
            return response_body

        # print(all_files)
        # return
        all_df = []
        for f in all_files:
            df = pd.read_csv(f, sep=',', dtype={'证券代码': str, '股东账号': str})
            file_name = f.split('/')[-1]
            date = file_name.split('.')
            YEARS = re.findall(r'\d{4}', date[0])
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
        #response_body = '{'
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            response_body = response_body + '"' + str(index) + '":{"code":"'+stock_code+'","date":"'\
                + row['成交日期']+'","num":'+str(row['当前数量'])+'}'
            if index < row_num - 1:
                response_body = response_body + ','
        print(response_body)
        response_body = response_body + '}}'
        return response_body
