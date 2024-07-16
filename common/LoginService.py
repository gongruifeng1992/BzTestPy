# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:LoginService.py
@data:2024/7/5 9:21 上午
"""
import time

import jsonpath

from common.ProcessCaseInfo import ProcessCaseInfo
from utils.FileReadUtil import FileReadUtil
from utils.LoggerUtil import logger
from utils.RedisUtil import RedisUtil
from utils.RequestUtil import RequestUtil



class LoginService:
    def __init__(self):
        self.name="LoginService"

    def get_curr_timestamp(self):
        timestamp=str(time.time() * 1000)[0:13]
        data={"batchNo":timestamp}
        FileReadUtil("./extract.yaml").exist_key_yaml(data)
        return timestamp

    def get_redis_verifycode(self):
        conf = FileReadUtil("./pytest.ini").read_conf("test")
        timestamp = FileReadUtil("./extract.yaml").read_yaml()["batchNo"]
        code = RedisUtil(conf).get_value("image:" + timestamp)
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

    def write_token(self):
        conf = FileReadUtil("./pytest.ini").read_conf("test")
        """获取token，并写入pytest.ini"""
        timestamp = str(time.time() * 1000)[0:13]
        source_data = FileReadUtil("pytest.ini").read_conf("test")
        account = source_data["account_token"]
        password = source_data["password_token"]

        headers = ProcessCaseInfo().process_headers()
        # 1-获取图片验证码
        url = source_data["host"] + "/service/service-basic/image/" + str(timestamp)
        RequestUtil().sendRequest(url=url, method="get", headers=headers)

        # 2-从redis读取验证码
        code = RedisUtil(conf).get_value("image:" + str(timestamp))

        # 3-登录获取token，并写入pytest.ini
        url1 = source_data["host"] + "/service/service-basic/account/login"
        json_data = {
            "account": account,
            "batchNo": timestamp,
            "code": code,
            "passwd": password
        }
        res = RequestUtil().sendRequest(url=url1, method="post", headers=headers, json=json_data)
        token = jsonpath.jsonpath(res, '$.text.data.token')

        conf1 = FileReadUtil("./pytest.ini").read_conf_all()
        try:
            is_exist = conf1["test"]["token"]

        except Exception as e:
            logger.info("pytest.ini中无token，写入：" + token[0])
            conf1.set("test", "token", token[0])
            FileReadUtil("./pytest.ini").write_conf(conf1,"w")




