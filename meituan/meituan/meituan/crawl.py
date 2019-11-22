# -*- coding: utf-8 -*-
"""
@Author: yqbao
@GiteeURL: https://gitee.com/yqbao
@name:XXX
@Date: 2019/11/19 10:40
@Version: v.0.0
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from meituan.spiders.waimai_list import WaimaiSpider
from meituan.spiders.waimai_detail import WaimaiDetailSpider
from meituan.spiders.waimai_comments import WaimaiCommentsSpider
from meituan.spiders.waimai_info import WaimaiInfoSpider
from meituan.spiders.waimai_safety import WaimaiSafetySpider


def crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl(WaimaiCommentsSpider)
    process.start()


if __name__ == '__main__':
    crawl()
