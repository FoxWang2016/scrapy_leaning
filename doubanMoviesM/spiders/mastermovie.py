# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request

from doubanMoviesM.items import DoubanmoviesmItem

"""
    分布式爬虫：主爬虫，用于爬取待爬信息的url，将信息保存到redis，供子爬虫爬取
                此爬虫支持断点续爬，如果中断，重启即可
"""
class MastermovieSpider(scrapy.Spider):
    name = 'mastermovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/tag/']
    home = 'https://movie.douban.com'

    def parse(self, response):
        for a in range(0, 10000, 20):
            movie_info_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影&start={}'.format(a)
            yield Request(url=movie_info_url, callback=self.get_movie_info)

    def get_movie_info(self, response):
        infos = json.loads(response.body)
        datas = infos.get('data')
        for data in datas:
            item = DoubanmoviesmItem()
            item['url'] = data.get('url')
            yield item
