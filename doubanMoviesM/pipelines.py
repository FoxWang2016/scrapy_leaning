# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class DoubanmoviesmPipeline(object):

    def __init__(self):
        redis_url = 'redis://:@localhost:7379/'
        self.r = redis.Redis.from_url(redis_url, decode_responses=True)

    def process_item(self, item, spider):
        url = item['url']
        isin = self.r.sadd("doubanmovie:douban_already_urls", url)
        if isin:
            self.r.lpush("doubanmovie:douban_urls", url)
        return item

