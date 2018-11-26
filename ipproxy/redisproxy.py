from ipproxy.proxy import MasterProxy
import redis


class RedisProxy(MasterProxy):

    def __init__(self, url, home, proxy_max=20, restart_min=5, redis_db_name='ip_proxy'):
        super().__init__(url, home, proxy_max, restart_min)
        redis_url = 'redis://:@localhost:7379/'
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
        self.redis_db_name = redis_db_name

    def get_ip_pool(self):
        return self.redis.smembers(self.redis_db_name)

    def ip_pool_length(self):
        return self.redis.scard(self.redis_db_name)

    def ip_proxy_saver(self, ip):
        self.redis.sadd(self.redis_db_name, ip)

    def ip_proxy_deleter(self, ip):
        self.redis.srem(self.redis_db_name, ip)

    def ip_random(self):
        return self.redis.srandmember(self.redis_db_name)


if __name__ == '__main__':
    xiciRedisProxy = RedisProxy('http://www.xicidaili.com/nn/', 'http://www.xicidaili.com')
    xiciRedisProxy.proxy_main(xiciRedisProxy)
