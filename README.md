# 免费代理获取
  获取网上的**有效**免费代理。
 
  
## 使用方法
 首先先确保安装了依赖包：
 ```
   # 终端运行
   pip install -r requirements.txt
```
### 一次性获取有效的代理
  非常简单， 直接使用proxy.py文件中的run_getter_and_tester函数， 即可
 返回一个有效的代理池集合(set)。


```python
    TEST_URL = 'https://wwww.baidu.com'
    data = run_getter_and_tester(TEST_URL)
    print(data)
```
返回结果：
```
finaly we got 17  validated proxies!
{'183.157.4.173:8118', '222.128.9.235:33428', 
 ...}

```
建议把TEST_URL改成你的目标爬虫网站

### 维持一个代理池
  考虑到免费代理的有效生命周期较短， 所以需要不断地获取免费代理->加入代理池（这里使用的是redis）->验证池中代理的有效性。
在设置完settings中的：
- TEST_URL （一般是爬虫的对象网站）
- INTERVAL （获取代理的间隔）
- FREEPROXY_REDIS_NAME （redis代理池名称）
运行方法：

```python
 # 终端运行
 python main.py
```

 
   

