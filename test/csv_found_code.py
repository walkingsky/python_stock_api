#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests
import json
sys.path.append("..")


def getCode(key):
    base_url = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=0&key=' + key
    res = requests.get(base_url)
    try:
        if(res.status_code == 200):
            # print(res.text)
            return json.loads(res.text)['Datas']['FundList'][0]['CODE']
        return ''
    except:
        return ''


if __name__ == "__main__":
    fo = open("../temp_data/基金交易记录.csv", "r", encoding="utf-8")
    fw = open("../temp_data/1.csv", "w", encoding="utf-8")
    str = ','

    lines = fo.readlines()

    for line in lines:

        datas = line.split(str)
        print(datas)
        if datas[1] == '':
            print('null')
            for line2 in lines:
                temp = line2.split(str)
                if datas[0] == temp[0] and temp[1] != '':
                    datas[1] = temp[1]
                    break
            if datas[1] == '':
                code = getCode(datas[0])
                if code != '':
                    datas[1] = code
                    for line2 in lines:
                        temp = line2.split(str)
                        if datas[0] == temp[0] and temp[1] == '':
                            temp[1] = code
                            line2 = str.join(temp)

        print(datas)
        lineNew = str.join(datas)

        fw.write(lineNew)

    # 关闭文件
    fo.close()
    fw.close()
