# -*- coding: utf-8 -*-
import re

from scrapy_redis.spiders import RedisSpider
from doubanMovies.items import DoubanmoviesItem


class DoubanmovieSpider(RedisSpider):
    name = 'doubanmovie'
    # allowed_domains = ['movie.douban.com']
    # start_urls = ['https://movie.douban.com/subject/4920528/']
    redis_key = 'doubanmovie:douban_urls'

    sql = 'insert into douban_spider_mv(movie_name, movie_type, director, movie_info,' \
          ' synopsis, rating_nums, url, pl) values(%s, %s, %s, %s, %s, %s, %s, %s)'

    def parse(self, response):
        item = DoubanmoviesItem()
        item['movie_name'] = response.xpath('//h1[1]//span[@property="v:itemreviewed"]/text()').extract()[0]
        item['movie_type'] = response.xpath("//div[@id='info']/span[5]/text()").extract()[0]
        item['director'] = response.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()").extract()[0]
        item['rating_nums'] = response.xpath("//strong[@class='ll rating_num']/text()").extract()[0]
        item['url'] = response.url
        report = response.xpath("//div[@id='link-report']/span[@class='all hidden']/text()").extract()
        synopsis = ''
        if report:
            report = report
        else:
            report = response.xpath("//div[@class='related-info']/div[@id='link-report']"
                                  "/span[@property='v:summary']/text()").extract()
        for rep in report:
            synopsis = synopsis + rep.replace('\n', '').strip()
        item['synopsis'] = synopsis
        movie_info = response.xpath("//div[@id='info']").extract()[0]
        item['movie_info'] = movie_info.replace('\n', '').strip()

        item['pl'] = re.findall('(\w*[0-9]+)\w*',
                                response.xpath("//div[@id='comments-section']/div[@class='mod-hd']"
                                               "/h2/span[@class='pl']/a/text()").extract()[0])[0]

        return item
        # item['area'] = scrapy.Field()
        # item['language'] = scrapy.Field()


