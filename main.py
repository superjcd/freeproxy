from proxy import run_getter_and_tester, ProxyTester
from utilis import run_after_secs, dump2formal
from ProxyStore import RedisProxyStore
from settings import TEST_URL, INTERVAL, FREEPROXY_REDIS_NAME
import threading
import pickle

rp = RedisProxyStore(FREEPROXY_REDIS_NAME)
event = threading.Event()

@run_after_secs(INTERVAL)
def check_proxies():
    '''
     检查redis中的proxies的有效性， 舍弃无效proxies
    :return:
    '''
    print('start check proxies')
    proxies = rp.get_all()  # 获取的是二进制数据（dumped data）
    if proxies:
        formal_proxies = dump2formal(proxies) # 正常的proxies数据
        # print(formal_proxies)
        pt = ProxyTester(collections=set(formal_proxies), test_url=TEST_URL)
        # 验证proxy是否有效
        pt.run()
        # 删除无效代理
        for proxy in proxies:
            _proxy = pickle.loads(proxy)
            if _proxy not in pt.validatepool:
                rp.delete(proxy)
    else:
        print('Empty Proxies Pool')
    event.set()  # 解除阻塞


@run_after_secs(INTERVAL)
def get_proxies():
    '''
     从网上获取
    :return:
    '''
    event.wait()  # 阻塞一下
    print('start get proxies')
    free_proxies = run_getter_and_tester(TEST_URL)
    for proxy in free_proxies:
        rp.add(pickle.dumps(proxy))



if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=check_proxies)
    threads.append(t1)

    t2 = threading.Thread(target=get_proxies)
    threads.append(t2)

    for t in threads:
        t.start()







