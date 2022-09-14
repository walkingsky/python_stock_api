### 股票行情工具的后端接口



前端项目地址：https://github.com/walkingsky/vue_stock_view



#### 1.数据准备

- 股票历史交易记录文件：从广发操盘手客户端导出历史交易记录（文件名匹配 “\*历史成交-\*.csv”，比如广发操盘手-历史成交-1.csv），存放到固定目录DIR
- 股票持仓记录文件：从广发操盘手客户端导出历史交易记录（文件名“广发操盘手-持仓.csv”），存放到固定目录DIR

#### 2.配置

- （必须）修改stockService.py 文件中的getPath 函数，返回上一步的目录DIR 

  ```
  def getPath(self):
          if os.path.exists('/data'):
              path = "/data/tools/python/stock_csv"
          else:
              path = "F:/study/python/stock_csv"
          return path

- ​	修改app.py 中的flask执行参数，比如端口号（也可以保持默认不修改）

  `app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)`

#### 3.安装库

`pip install -r requirements.txt`

#### 4.执行

`python app.py`

#### 备注说明：

- python版本3.8.10

- flask使用开发模式运行，对高并发运行支持的不是很好，所以前端的“行业行情分析”做了获取数据的数量限制。如果将该代码部署到了支持高并发的环境中，可适当调高行业数量和行业内股票数量的限制。


```\# 行业数量默认限制
# 行业数量默认限制
limitIn = 5
# 行业内股票数量默认限制
limitStock = 10
```
