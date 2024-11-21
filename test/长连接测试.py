#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "walkingsky"

from multiprocessing import Process,Pipe
import requests
import time

url='https://88.push2.eastmoney.com/api/qt/ulist/sse?' +\
    'secids=0.002902,1.600833,0.003031,0.300274' +\
    '&fields=f12,f13,f14,f19,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100' +\
    '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'
    # '&invt=3&ut=fa5fd1943c7b386f172d6893dbfba10b&fid=&po=1&pi=0&pz=30&mpi=6000&dect=1'

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

s = requests.session()

#
r = s.get(url,stream=True,headers=headers)

print(r.status_code)
# print(r)

# delimiter 分隔符，decode_unicode
for line in r.iter_lines(chunk_size=1024,delimiter="\n",decode_unicode=True):
    if line:
        print(line)
# data = r.json()
# print(data)

    
while True:
    time.sleep(5)

s.close()