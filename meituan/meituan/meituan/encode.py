# -*- coding: utf-8 -*-
"""
@Author: yqbao
@GiteeURL: https://gitee.com/yqbao
@name:XXX
@Date: 2019/11/20 10:31
@Version: v.0.0
"""
import base64
import zlib
import json
import random


class MeituanEncryption:
    def __init__(self, ts, data, url):
        self.url = url
        self.ts = ts
        self.data = data
        br_vd_list = [
            [376, 722], [320, 568], [414, 736], [375, 667], [376, 578],
            [768, 1024], [412, 732], [375, 812], [1024, 1366]
        ]
        self.brVD = random.choice(br_vd_list)
        self.brR = [self.brVD, self.brVD, 24, 24]

    def get_sign(self):
        """
        构造sign（请求的URL中一个参数）
        由各种乱七八糟的信息组成的字典，进行URL编码，URL参数拼接，然后压缩
        """
        clean_data = {
            key: value
            for key, value in self.data.items()
            if key not in ["uuid", "platform", "partner"]
        }
        sign_data = []
        for key in sorted(clean_data.keys()):
            sign_data.append(key + "=" + str(clean_data[key]))
        sign_data = "&".join(sign_data)
        compressed_data = self.compress_data(sign_data)
        return compressed_data

    def encode_token(self):
        """
        生成token
        :return:
        """
        token_dict = {
            "rId": 101701,
            "ver": "1.0.6",
            "ts": self.ts,
            "cts": self.ts + 100 * 1000,
            "brVD": self.brVD,
            "brR": self.brR,
            "bI": [self.url, ''],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "aM": '',
            "sign": self.get_sign()
        }
        compressed_data = self.compress_data(token_dict)
        return compressed_data

    def compress_data(self, data):
        """
        压缩token和sign参数的方法
        转为JSON字符串，使用zlib压缩，再使用base64编码
        """
        json_data = json.dumps(data, separators=(',', ':')).encode("utf-8")
        compressed_data = zlib.compress(json_data)
        base64_str = base64.b64encode(compressed_data).decode()
        return base64_str
