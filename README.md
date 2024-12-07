### 股票行情工具的后端接口



前端项目地址：https://github.com/walkingsky/vue_stock_view



#### 1.数据准备

- 股票历史交易记录文件：从广发操盘手客户端导出历史交易记录（文件名匹配 “\*历史成交-\*.csv”，比如广发操盘手-历史成交-1.csv），存放到固定目录DIR
- 股票持仓记录文件：从广发操盘手客户端导出历史交易记录（文件名“广发操盘手-持仓.csv”），存放到固定目录DIR

#### 2.配置

- （必须）修改config.py 文件中的路径参数，使其匹配前端页面项目的保存路径 

  ```
  # 前端static目录
  WEB_STATIC_DIR = '../../frontend/vue_stock_view/dist/static'
  # 前端页面目录
  WEB_DIR = '../../frontend/vue_stock_view/dist'
  
- ​	根据实际需求修改config.py 文件中的其他配置参数，也可以保持默认

  

#### 3.安装库

`pip install -r requirements.txt`

#### 4.安装Redis server，并启动redis服务

#### 5.执行

启动后台数据服务

```
python python services\stockStatus2Redis.py
```

启动web主程序

```
python app.py
```



#### 备注说明：

- python版本3.8.10

- flask使用开发模式运行，对高并发运行支持的不是很好，所以前端的“行业行情分析”做了获取数据的数量限制。如果将该代码部署到了支持高并发的环境中，可适当调高行业数量和行业内股票数量的限制。


```\# 行业数量默认限制
# 行业数量默认限制
limitIn = 5
# 行业内股票数量默认限制
limitStock = 10
```
