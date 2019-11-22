# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import json


class MeituanPipeline(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.read = redis.Redis(host=host, port=port, db=db, decode_responses=True)  # 其余均采用默认值

    @classmethod
    def from_crawler(cls, crawler):
        """信息注入，包括设置MongoDB地址与库名"""
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
        )

    def process_item(self, item, spider):
        if spider.name == "waimai_list":
            poi_id = item['poi_id']
            if poi_id:
                # sadd 将指定的成员添加到集合中的key，已经是此集合成员的将被忽略
                if self.read.sadd('meituan_shop:id', poi_id):
                    self.read.lpush('meituan:detail', json.dumps(item._values))
                    self.read.lpush('meituan:comments', json.dumps(item._values))
                    self.read.lpush('meituan:info', json.dumps(item._values))
                    self.read.lpush('meituan:safety', json.dumps(item._values))
            else:
                self.read.lpush('meituan:no_meta', json.dumps(item._values))
