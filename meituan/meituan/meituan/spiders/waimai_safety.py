# -*- coding: utf-8 -*-
import json
import six
import random
from datetime import datetime

from scrapy import FormRequest
from scrapy_redis.spiders import RedisSpider
from meituan.settings import USER_AGENTS_LIST


def bytes_to_str(s, encoding="utf-8"):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


class WaimaiSafetySpider(RedisSpider):
    name = 'waimai_safety'
    redis_key = "meituan:safety"
    ts = int(datetime.now().timestamp() * 1000)
    ua = random.choice(USER_AGENTS_LIST)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded",
        "Host": "i.waimai.meituan.com",
        "Origin": "https://i.waimai.meituan.com",
        "Pragma": "no-cache",
        "Referer": '',
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make_request_from_data(self, data):
        meta = bytes_to_str(data, self.redis_encoding)
        meta = json.loads(meta)
        headers = self.headers
        uuid = meta.get("uuid")
        shop_id = meta.get("poi_id")
        lat = meta.get("lat")
        long = meta.get("long")
        headers["User-Agent"] = self.ua
        headers["Referer"] = "https://h5.waimai.meituan.com/waimai/mindex/menu?" \
                             "mtShopId={}&source=shoplist&initialLat={}&initialLng={}".format(shop_id, lat, long)
        headers[
            "Cookie"] = 'terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_latlng=30678132,104028975; w_actual_lat=0; w_actual_lng=0; w_visitid=3e6f3d23-cf31-4625-956f-739b7bc8f5fb; au_trace_key_net=default; _lxsdk_cuid=16e877df7bf77-0d7aa84a0f2d0e-277e2849-422f8-16e877df7c0c8; iuuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; mt_c_token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; oops=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; userId=281544318; wm_order_channel=default; utm_source=; _lxsdk=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; openh5_uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; w_token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; openh5_uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; igateApp=%3C%25%3D%20htmlWebpackPlugin.options.iGateAppKey%20%25%3E; logan_custom_report=; w_uuid=NWZjneb0wiqHkSyf51YEy0Y9WRc64UiKEPq7wWSQQbocNSuLg6Tm5j3D0_vPFPCm; cssVersion=d7835dae; logan_session_token=mz6emfix0cn42cuq3z27; _lx_utm=utm_source%3D; _lxsdk_s=16e877df5dc-60e-b5c-496%7C%7C24'

        url = "https://i.waimai.meituan.com/openh5/poi/comments?_={}".format(self.ts)
        form_data = {
            "wm_poi_id": uuid
        }
        return FormRequest(url, formdata=form_data, headers=headers, dont_filter=True)

    def parse(self, response):
        with open("safety.json", "w", encoding="utf-8") as f:
            f.write(response.text)
