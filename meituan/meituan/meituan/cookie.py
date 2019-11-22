# -*- coding: utf-8 -*-
"""
@Author: yqbao
@GiteeURL: https://gitee.com/yqbao
@name:XXX
@Date: 2019/11/20 16:19
@Version: v.0.0
"""


def structure_cookie():
    cook = {}
    cookies = """terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_latlng=30678132,104028975; w_actual_lat=0; w_actual_lng=0; au_trace_key_net=default; _lxsdk_cuid=16e877df7bf77-0d7aa84a0f2d0e-277e2849-422f8-16e877df7c0c8; iuuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; mt_c_token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; oops=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; userId=281544318; wm_order_channel=default; utm_source=; _lxsdk=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; openh5_uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; w_token=vkpHZbaI5YsLN45Q5WXxpaiukXwAAAAAgQkAAIMNIiyaRUXsJvXCJpjcB9FeHi5nAwQYYcyoC8Hp0vOilJy7U2iGIpAPyeGVipq2Ug; openh5_uuid=E6DC319C16A2B1DF4AB38F60069E1556A9AFDCF03B6D7185EBE8FB17C9279F87; igateApp=%3C%25%3D%20htmlWebpackPlugin.options.iGateAppKey%20%25%3E; logan_custom_report=; w_uuid=NWZjneb0wiqHkSyf51YEy0Y9WRc64UiKEPq7wWSQQbocNSuLg6Tm5j3D0_vPFPCm; logan_session_token=icpywf7xy1kc53iqopb2; w_visitid=e82a94e4-5d40-4fa7-aba7-592f22b0a57a; cssVersion=56d5201e; _lx_utm=utm_source%3D; _lxsdk_s=16e87e5463c-e06-a99-d04%7C281544318%7C6""".split(
        ";")
    for cookie in cookies:
        f = cookie.split("=")
        if f[0].strip() == "w_utmz":
            cook[f[0]] = '='.join(f[1:])
        else:
            cook[f[0]] = f[1]
    return cook
