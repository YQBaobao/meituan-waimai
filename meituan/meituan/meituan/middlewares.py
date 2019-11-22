# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import random
import json
import time
import redis

from json.decoder import JSONDecodeError
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from meituan import settings


class MeituanDownloaderMiddleware(UserAgentMiddleware):
    """用于设置随机UA和代理IP的中间件"""

    def __init__(self, user_agent='', host='localhost', port=6379, db=0, url=None, enabled=False):
        super().__init__()
        self.user_agent = user_agent
        self.read = redis.Redis(host=host, port=port, db=db, decode_responses=True)  # 其余均采用默认值
        self.url = url
        self.enabled = enabled

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
            url=crawler.settings.get('PROXY_SERVER'),
            enabled=crawler.settings.get('PROXY_ENABLED'),
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        ua = random.choice(settings.USER_AGENTS_LIST)  # 随机获取UA
        request.headers['User-Agent'] = ua
        if self.enabled:
            ip_port = requests.get(self.url).text  # 获取代理
            request.meta['proxy'] = 'https://' + ip_port  # 设置代理
            try:
                if spider.name != "waimai_list":
                    json.loads(ip_port)
            except JSONDecodeError:
                self.read.lpush('book:book_url', request.url)
                time.sleep(2)


class MeituanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
