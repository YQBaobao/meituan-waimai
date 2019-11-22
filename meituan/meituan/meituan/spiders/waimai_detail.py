# -*- coding: utf-8 -*-

import json
import six
import random
from datetime import datetime

from scrapy import FormRequest
from scrapy_redis.spiders import RedisSpider
from meituan.settings import USER_AGENTS_LIST


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


class WaimaiDetailSpider(RedisSpider):
    name = 'waimai_detail'
    redis_key = 'meituan:detail'
    ts = int(datetime.now().timestamp() * 1000)
    ua = random.choice(USER_AGENTS_LIST)
    headers = {
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

    def make_request_from_data(self, data):
        meta = bytes_to_str(data, self.redis_encoding)
        meta = json.loads(meta)
        headers = self.headers
        shop_id = meta.get('poi_id')
        lat = meta.get("lat")
        long = meta.get("long")
        headers["User-Agent"] = self.ua
        headers["Referer"] = "https://h5.waimai.meituan.com/waimai/mindex/menu?" \
                             "mtShopId={}&source=shoplist&initialLat={}&initialLng={}".format(shop_id, lat, long)
        url = "https://i.waimai.meituan.com/openh5/poi/food?_={}".format(self.ts)
        form_data = {
            "geoType": "2",
            "mtWmPoiId": meta.get("poi_id"),
            "dpShopId": "-1",
            "source": "shoplist",
            "skuId": '',
            "uuid": meta.get("uuid"),
            "platform": "3",
            "partner": "4",
            "originUrl": headers["Referer"],
            "riskLevel": "71",
            "optimusCode": "10",
            "wm_latitude": lat,
            "wm_longitude": long,
            "wm_actual_latitude": '',
            "wm_actual_longitude": '',
            "openh5_uuid": meta.get("uuid"),
            "_token": meta.get("token"),
        }
        return FormRequest(url, formdata=form_data, headers=headers, dont_filter=True)

    def parse(self, response):
        with open("detail.json", "a", encoding="utf-8") as f:
            f.write(response.text)
