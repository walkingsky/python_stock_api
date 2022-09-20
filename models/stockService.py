#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'walkingsky'


import os
import glob
import time
import pandas as pd
import requests
import numpy as np


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
        # print(response_body)
        return response_body

    def getHistoryHold(self):
        '''
        从csv文件中，获取所有持仓过的股票数据
        '''
        path = self.getPath()
        all_files = glob.glob(os.path.join(path, "*历史成交-*.csv"))
        if not all_files:
            return '{}'

        all_df = []
        for f in all_files:
            df = pd.read_csv(f, sep=',',  dtype={'证券代码': str})
            all_df.append(df)

        merged_df = pd.concat(all_df, ignore_index=True, sort=True)
        merged_df = merged_df[merged_df['业务名称'].isin(["证券买入", "证券卖出", "新股入账"])]
        # print(merged_df)

        merged_df['证券代码'] = merged_df['证券代码'].str.strip()
        merged_df['证券名称'] = merged_df['证券名称'].str.strip()

        merged_df['交易金额'] = np.where(
            merged_df['买卖方向'] == '买入', merged_df['交易金额'], -merged_df['交易金额'])
        # merged_df['成交数量'] = np.where(
        #    merged_df['买卖方向'] == '买入', merged_df['成交数量'], -merged_df['成交数量'])
        res_df = merged_df.groupby(
            ['证券代码', '市场'], as_index=False).sum()
        # print(res_df)
        merged_df = merged_df.drop(
            columns=['买卖方向', '交易金额', '业务名称', '成交编号', '成交价格', '成交数量', '成交日期', '成交时间', '股东账号']).drop_duplicates(subset=['证券代码', '市场'], keep='first')

        # res_df = pd.concat([res_df, merged_df], axis=1,
        #                   join='inner', ignore_index=True)

        res_df = pd.merge(res_df, merged_df,  on=[
            '证券代码', '市场'])
        # print(res_df)
        row_num = res_df.shape[0]
        json_str = '{"code":200,"results":['
        for index, row in res_df.iterrows():
            json_str = json_str + '{"key":'+str(index)+',"code":"'+row['证券代码']+'","name":"'\
                + row['证券名称'] + '","market":"'+row['市场']+'","price":"' + \
                str(row['交易金额'])+'","num":"'+str(row['成交数量'])+'"}'
            if index < row_num - 1:
                json_str = json_str + ','

        json_str = json_str + ']}'
        return json_str

    def getHistory(self, stock_code, market):
        '''
        通过股票代码，市场，从csv列表文件中获取股票的历史交易数据
        '''
        path = self.getPath()
        all_files = glob.glob(os.path.join(path, "*历史成交-*.csv"))
        if not all_files:
            return '{}'

        # print(all_files)
        # return
        all_df = []
        for f in all_files:
            df = pd.read_csv(f, sep=',', dtype={
                             '证券代码': str, '股东账号': str, '成交日期': str})
            '''
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
            '''
            all_df.append(df)

        merged_df = pd.concat(all_df, ignore_index=True, sort=True)
        merged_df['证券代码'] = merged_df['证券代码'].str.strip()
        result_df = merged_df[(merged_df['市场'] == market) & (
            merged_df['证券代码'] == stock_code)].reset_index(drop=True)
        # print(result_df)
        response_body = '{"code":200,"results":['
        row_num = result_df.shape[0]
        for index, row in result_df.iterrows():
            temp = list(row['成交日期'].strip())
            temp.insert(4, '-')
            temp.insert(7, '-')
            response_body = response_body + '{"code":"'+stock_code+'","date":"'\
                + ''.join(temp)+'","time":"'+row['成交时间'].strip()+'","sell_buy":"'+row['买卖方向']+'","price":' + \
                str(row['成交价格'])+',"num":'+str(row['成交数量'])+'}'
            if index < row_num - 1:
                response_body = response_body + ','
        response_body = response_body + ']}'
        return response_body

    def getStockByCode126(self, code):
        '''
            获取股票的是实时信息，126数据接口
            #code 参数，code 可以是一个，也可以是用逗号分隔的多个。 要带上市场简写，比如 sh600036,sz300301
        '''
        base_url = 'http://img1.money.126.net/data/hs/time/today/'+code+'.json'
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def getStockByCodeEastM(self, code):
        '''
            获取股票的是实时信息，东财数据接口
            #code 参数，code 可以是一个，也可以是用逗号分隔的多个。 要带上市场简写，比如 sh600036,sz300301
        '''
        base_url = 'https://push2.eastmoney.com/api/qt/stock/trends2/get?secid='+code + \
            '&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&iscr=0'
        res = requests.get(base_url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def getStockHistoryData(self, code):
        # 获取股票的历史行情
        today = time.strftime("%Y%m%d", time.localtime())
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&fqt=0&end=' + \
            today + '&klt=101&secid=' + code + '&fqt=1&lmt=1000'
        res = requests.get(url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def getIndustryData(self, kind, sort, pz):
        # 获取行业排行数据
        fid = 'f3'
        if kind != 'fluctuate':
            fid = 'f62'
        po = '1'
        if sort != 'asc':
            po = '0'

        url = 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz='+str(pz)+'&po=' + po + '&np=1&fltt=2&invt=2&fid=' + fid + \
            '&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222'

        res = requests.get(url)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def getIndustryInfoData(self, industryCode, kind, sort, pz):
        # 获取行业内股票排行数据
        fid = 'f3'
        if kind != 'fluctuate':
            fid = 'f62'
        po = '1'
        if sort != 'asc':
            po = '0'

        url = "https://push2.eastmoney.com/api/qt/clist/get?fid=" + fid + "&po=" + po + "&pz="+str(pz)+"&pn=1&np=1&fltt=2&invt=2&fs=b:" + \
            industryCode + "&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"

        res = requests.get(url)
        # print(res)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result

    def getIndustryHistoryData(self, industryCode):
        # 获取行业日K曲线数据
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=90.'+industryCode + \
            '&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&end=20500101&&lmt=300'

        res = requests.get(url)
        # print(res)
        result = {}
        if(res.status_code == 200):
            return res.text
        return result
