#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

import threading
import requests
import time,json
import redis
import sys
sys.path.append('..')
from config import REDIS_HOST,REDIS_PORT


redisClient = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=0,decode_responses=True)

headers ={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'qgqp_b_id=04d98930562bb8f118b93bd3745149ec; st_pvi=28821874947718; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sp=2020-08-20%2011%3A39%3A47',
    'Host':'88.push2.eastmoney.com',
    'Pragma':'no-cache',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}
# 转换数据，将变化的数据重写到datajson
def convertData(codes,dataStr,dataJsonOld):
    codeArry = codes.split(',')   
    dataJson = json.loads(dataStr)
    dataJsonNew = {}
    # f2: 当前股价*100 f3:涨幅*100 f4:涨跌额*100 f5:总手 f6:成交额
    # f7: 振幅*100 f8: 换手率*100 f9:市盈率*100 f10:量比*100 f12:股票代码
    # f13: 股市（0、1、2） f14:股票名称 f18:昨日收盘价*100 f31:买入价*100
    # f32:卖出价*100 f100:行业板块 f112:每股收益
    stockKeysArray = ['f2','f3','f4','f12','f13','f14','f18','f112']
    if not (dataJson['data'] is None):
        for key in codeArry:
            indexKey = str(codeArry.index(key))
            if  indexKey in dataJson['data']['diff']:
                dataJsonNew[key] = {}
                for stockKey in stockKeysArray:
                    if stockKey in dataJson['data']['diff'][indexKey]:
                        dataJsonNew[key][stockKey] = dataJson['data']['diff'][indexKey][stockKey]
                    else:
                        dataJsonNew[key][stockKey] = dataJsonOld[key][stockKey]
            else:
                dataJsonNew[key] = dataJsonOld[key]
    else:
        dataJsonNew = dataJsonOld
    
    return dataJsonNew



def getStockInfoThreading(codes,clientId):
    global runingThreads
    threadingName = threading.currentThread().getName()
    print('threading name is:(%s),codes is:(%s),clientId is:(%s)'%(threadingName,codes,clientId))

    url='https://88.push2.eastmoney.com/api/qt/ulist/sse?' +\
        'secids=' + str(codes) +\
        '&fields=f12,f13,f14,f19,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100' +\
        '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'
        # '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'
        # 'secids=0.002902,1.600833,0.003031,0.300274' +\

    s = requests.session()
    r = s.get(url,stream=True,headers=headers)
    n = 1
    dataJson = json.loads('{}')
    # delimiter 分隔符，decode_unicode
    for line in r.iter_lines(chunk_size=1024,delimiter="\n",decode_unicode=True):
        if line:
            # f2: 当前股价*100 f3:涨幅*100 f4:涨跌额*100 f5:总手 f6:成交额
            # f7: 振幅*100 f8: 换手率*100 f9:市盈率*100 f10:量比*100 f12:股票代码
            # f13: 股市（0、1、2） f14:股票名称 f18:昨日收盘价*100 f31:买入价*100
            # f32:卖出价*100 f100:行业板块 f112:每股收益
            
            #print(line)
            #去掉 开头字符，变成标准json字符串
            dataStr = str(line).replace('data: ','',1)
            dataJson = convertData(codes,dataStr,dataJson)
            print(dataJson)
            redisClient.rpush(clientId + '_msg',json.dumps(dataJson,ensure_ascii=False))
            newCodes = redisClient.get(clientId) 
            n = n + 1 
            print(runingThreads)    
            if(newCodes == None or newCodes == '' or newCodes != codes):
                runingThreads.remove(clientId+str(codes))
                s.close()
                print('退出线程:'+threadingName)
                return
            print('count is : %d'%(n))
    '''       
    while True:
        stop_codes = redisClient.rpop('stop_codes')
        if (stop_codes == codes):
            s.close()
            return
    '''

    

if __name__ == '__main__':
    runingThreads = []     
    while True:
        clients = redisClient.smembers('connect_ids')
        # print(clients)
        for clinet in clients:                        
            codes = redisClient.get(clinet)        
            if(not ( codes == None or codes == '' )):
                threadName=clinet + codes
                if threadName in runingThreads:
                    pass
                else:
                    print('get codes from redis:' + str(codes))
                    n = threading.Thread(target=getStockInfoThreading,name=threadName,args=(str(codes),clinet))
                    n.start()
                    runingThreads.append(clinet + codes)
        
        print(runingThreads)

        time.sleep(1)
