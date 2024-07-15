# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:abdc.py
@data:2024/7/15 8:58 上午
"""
if __name__ == '__main__':
    str="[{\"key\":\"User-Agent\",\"value\":\"Mozilla/5.0 (Linux; Android 12; SM-N9860 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220903 Mobile Safari/537.36 MMWEBID/9048 MicroMessenger/8.0.28.2240(0x28001C35) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android\",\"enabled\":true}]"
    print(str.replace("\"",""))