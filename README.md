# 免费代理获取
  获取网上的**有效**免费代理。
  
## 使用方法
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
 
 
   

