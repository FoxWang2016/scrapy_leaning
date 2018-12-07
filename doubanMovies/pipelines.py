# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.utils.project import get_project_settings

class DoubanmoviesPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        self.host = settings.get('MYSQL_HOST')
        self.user = settings.get('MYSQL_USER')
        self.pwd = settings.get('MYSQL_PASSWD')
        self.name = settings.get('MYSQL_DBNAME')
        self.charset = settings.get('MYSQL_CHARSET')

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.pwd,
            db=self.name,
            charset=self.charset
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        movie_name = item['movie_name']
        director = ",".join(item['director'])
        url = item['url']

        try:
            rating_nums = item['rating_nums']
        except:
            rating_nums = 0

        try:
            movie_type = item['movie_type']
        except:
            movie_type = ''

        try:
            movie_info = item['movie_info']
        except:
            movie_info = ''
        try:
            synopsis = item['synopsis']
        except:
            synopsis = ''
        try:
            pl = item['pl']
        except:
            pl = 0

        list = [movie_name, movie_type, director, movie_info, synopsis, rating_nums, url, pl]

        try:
            self.cur.execute(spider.sql, list)
        except Exception as e:
            print(e)
            self.conn.rollback()
        else:
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
