# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    movie_type = scrapy.Field()
    director = scrapy.Field()
    movie_info = scrapy.Field()
    synopsis = scrapy.Field()
    rating_nums = scrapy.Field()
    url = scrapy.Field()
    pl = scrapy.Field()

