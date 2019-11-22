# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime

from meituan import settings
from meituan.mysqlhelper import *
from meituan.settings import USER_AGENTS_LIST
from meituan.encode import MeituanEncryption

from scrapy import Item
from scrapy import Request, FormRequest
from scrapy_redis.spiders import RedisSpider


class WaimaiSpider(RedisSpider):
    name = "waimai_list"
    ts = int(datetime.now().timestamp() * 1000)
    allowed_domains = ["waimai.meituan.com"]

    headers_1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "h5.waimai.meituan.com",
        "Pragma": "no-cache",
        "Referer": '',
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    headers_2 = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": '',
        "Host": "i.waimai.meituan.com",
        "Origin": "https://h5.waimai.meituan.com",
        "Pragma": "no-cache",
        "Referer": '',
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        uuid = settings.UUID
        lat = "30678132"
        long = "104028975"
        headers = self.headers_1
        url = "https://h5.waimai.meituan.com/waimai/mindex/home"
        ua = random.choice(USER_AGENTS_LIST)
        headers["Referer"] = "https://h5.waimai.meituan.com/waimai/mindex"
        headers["User-Agent"] = ua
        yield Request(url, headers=headers, meta={"uuid": uuid, "lat": lat, "long": long, })

    def parse(self, response):
        meta = response.meta
        uuid = meta.get("uuid")
        lat = meta.get("lat")
        long = meta.get("long")
        post_data = {
            "geoType": "2",
            "multiFilterIds": "",
            "openh5_uuid": uuid,
            "optimusCode": "10",
            "originUrl": "https://h5.waimai.meituan.com/waimai/mindex/home"
                         "&partner=4&platform=3&rankTraceId=&riskLevel=71&sliderSelectCode="
                         "&sliderSelectMax=&sliderSelectMin=&sortId=0&startIndex=0&uuid={}"
                         "&wm_actual_latitude=0&wm_actual_longitude=0"
                         "&wm_latitude={}&wm_longitude={}".format(uuid, lat, long)
        }
        encryption = MeituanEncryption(ts=self.ts, data=post_data, url=response.url)
        meta["token"] = encryption.encode_token()
        return self.list_requests(meta)

    def list_requests(self, meta):
        uuid = meta.get("uuid")
        headers = self.headers_2
        headers["Referer"] = "https://h5.waimai.meituan.com/waimai/mindex/home"
        url = "https://i.waimai.meituan.com/openh5/homepage/poilist?_={}".format(self.ts)
        form_data = [{
            "startIndex": str(index),
            "sortId": "0",
            "multiFilterIds": '',
            "sliderSelectCode": '',
            "sliderSelectMin": '',
            "sliderSelectMax": '',
            "geoType": "2",
            "rankTraceId": '',
            "uuid": uuid,
            "platform": "3",
            "partner": "4",
            "originUrl": headers["Referer"],
            "riskLevel": "71",
            "optimusCode": "10",
            "wm_latitude": "0",
            "wm_longitude": "0",
            "wm_actual_latitude": meta.get("lat"),
            "wm_actual_longitude": meta.get("long"),
            "openh5_uuid": uuid,
            "_token": meta.get("token")
        } for index in range(0, 3)]
        ua = random.choice(USER_AGENTS_LIST)
        headers["User-Agent"] = ua
        for data in form_data:
            yield FormRequest(url, formdata=data, headers=headers, dont_filter=True, meta=meta,
                              callback=self.parse_shop_list)

    def parse_shop_list(self, response):
        data_item = Item()
        with open("list.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        meta = response.meta
        response = json.loads(response.text)
        shop_list = response.get("data").get("shopList")
        for shop in shop_list:
            mt_wm_poi_id = shop.get("mtWmPoiId")
            meta['poi_id'] = mt_wm_poi_id
            data_item._values = meta
            yield data_item
