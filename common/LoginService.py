# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:LoginService.py
@data:2024/7/5 9:21 上午
"""
import time

from utils.FileReadUtil import FileReadUtil
from utils.LoggerUtil import logger
from utils.RedisUtil import RedisUtil


class LoginService:
    def __init__(self):
        self.name="LoginService"

    def get_curr_timestamp(self):
        timestamp=str(time.time() * 1000)[0:13]
        data={"batchNo":timestamp}
        FileReadUtil("./extract.yaml").exist_key_yaml(data)
        return timestamp

    def get_redis_verifycode(self):
        timestamp = FileReadUtil("./extract.yaml").read_yaml()["batchNo"]

        code = RedisUtil().get_value("image:" + timestamp)
        print("----code"+code)
        FileReadUtil("./extract.yaml").exist_key_yaml({"code": code})
        return code





    def get_conf(self,section,key):
        data=FileReadUtil("./pytest.ini").read_conf(section)
        return data[key]

    def get_account(self):
        return LoginService().get_conf("test","account")

    def get_password(self):
        return LoginService().get_conf("test","password")



