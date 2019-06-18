import redis
from settings import REDIS_CONFIG


#  use class
class ProxyStore:
    def __init__(self, proxies):
        '''
        将数据存储在set中
        :param proxies:
        '''
        if not isinstance(proxies, set):
            raise TypeError('proxy must be set!')
        else:
            self.proxies = proxies

    def get_random(self):
        random_element = self.proxies.pop()
        self.proxies.add(random_element)
        return random_element

    def add(self, element):
        self.proxies.add(element)

    def pop(self):
        return self.proxies.pop()

    def delete(self, element):
        self.proxies.remove(element)

    def update(self, elements):
        if not isinstance(elements, set):
            raise TypeError('proxy must be set!')
        else:
            self.proxies = self.proxies | elements

    def __len__(self):
        return len(self.proxies)



class RedisProxyStore:
    '''
       将数据存储在redis的set中
    '''
    def __init__(self, key):
        self.conn = redis.Redis(host=REDIS_CONFIG.get('host'), port= REDIS_CONFIG.get('port'))
        self.skey = key

    def add(self, element):
        self.conn.sadd(self.skey, element)

    def pop(self):
        return self.conn.spop(self.skey)

    def delete(self, element):
        if self.conn.sismember(self.skey, element):
            self.conn.srem(self.skey, element)
            print(f'{element} has been removed')
        else:
            print(f'{element} is not in the set')

    def update(self, elements):
        if not isinstance(elements, set):
            raise TypeError('elements must be a set!')
        else:
            for element in elements:
                self.add(element)

    def get_random(self):
        random_element = self.pop()
        self.add(random_element)
        return random_element

    def __len__(self):
        return self.conn.scard(self.skey)






    
        



