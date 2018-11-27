from ipproxy.proxy import MasterProxy
import redis


class RedisProxy(MasterProxy):

    def __init__(self, url, home, proxy_max=20, restart_min=5, redis_db_name='ip_proxy',
                 redis_host="localhost", redis_port="6379", redis_password=''):
        super().__init__(url, home, proxy_max, restart_min)
        # redis_url = 'redis://:@localhost:7379/'
        # self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
        self.redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
        self.redis_db_name = redis_db_name

    '''获取代理ip池'''
    def get_ip_pool(self):
        return self.redis.smembers(self.redis_db_name)

    '''获取代理ip池长度'''
    def ip_pool_length(self):
        return self.redis.scard(self.redis_db_name)

    '''将ip插入代理ip池'''
    def ip_proxy_saver(self, ip):
        self.redis.sadd(self.redis_db_name, ip)

    '''从代理ip池中删除某个ip'''
    def ip_proxy_deleter(self, ip):
        self.redis.srem(self.redis_db_name, ip)

    def ip_random(self):
        return self.redis.srandmember(self.redis_db_name)


if __name__ == '__main__':
    xiciRedisProxy = RedisProxy('http://www.xicidaili.com/nn/', 'http://www.xicidaili.com', redis_port='7379')
    xiciRedisProxy.proxy_main(xiciRedisProxy)
