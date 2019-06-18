import re
import time
import asyncio
import aiohttp
import sys
from utilis import get_page, getHtmlTree, get_random_ua
from aiohttp import ClientError


VALID_STATUS_CODES = [200, 301, 302]


class ProxyGetter:
    def crawl_kuaidaili(self):
        for i in range(1, 6):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ', '')

    def crawl_ip3366(self):
        for page in range(1, 6):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(
                page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':' + port
                yield result.replace(' ', '')

    def crawl_ip3366(self):
        for i in range(1, 6):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ', '')

 

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile(
                '<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_goubanjia(self):
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass
    
    
    def crawl_mianfei(self,page_count=20):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]


class ProxyTester(object):
    def __init__(self, collections, test_url=None):
        '''
            collection 是一个set
        '''
        self.collections = collections
        self.test_url = test_url
        self.validatepool = set()
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                # 获取随机user_agent
                random_agent = get_random_ua()
                async with session.get(self.test_url, proxy=real_proxy, timeout=10, allow_redirects=False, headers=random_agent) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.validatepool.add(proxy)
                        print('代理可用', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                print('代理请求失败', proxy)
    
    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            test_proxies = self.collections
            loop = asyncio.get_event_loop()
            tasks = [asyncio.ensure_future(self.test_single_proxy(proxy)) for proxy in test_proxies] 
            loop.run_until_complete(asyncio.wait(tasks))
            sys.stdout.flush()
            time.sleep(3)
        except Exception as e:  
            print('测试器发生错误', e.args)



def run_getter_and_tester(test_url=None):
    '''同时运行代理获取函数及代理检测函数， 并返回可用代理.
    :return:  返回可用代理集合，代理格式- {ip adress}:{port}
    :param test_url: 测试代理可用性的http网站
    '''
    if 'https' not in str(test_url) or 'http' not in str(test_url):
        raise ValueError('请确认test_url的格式是否正确(一定要包含https或http)')
    proxy_pool = set()
    pg = ProxyGetter()
    try:
        for name in dir(pg):
            if name.startswith('crawl'):
                func = getattr(pg, name)
                for proxy in func():  # func is a generator
                    proxy_pool.add(proxy)
    except Exception:
        print('Some error happens here! Ignore for moment!')
    print(f'we got {len(proxy_pool)} proxies!')
    pt = ProxyTester(collections=proxy_pool, test_url=test_url)
    pt.run()
    print(f'finaly we got {len(pt.validatepool)}  validated proxies!')
    return pt.validatepool


if __name__ == '__main__': 
    TEST_URL = 'https://wwww.baidu.com'
    data = run_getter_and_tester(TEST_URL)
    print(data)

