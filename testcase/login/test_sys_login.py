# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:test_sys_login.py
@data:2024/7/4 2:11 下午
"""

import os.path

import allure
import pytest

from common.LoginService import LoginService
from common.ProcessCaseInfo import ProcessCaseInfo
from utils.AssertUtil import AssertUtil
from utils.ExtractUtil import ExtractUtil
from utils.FileReadUtil import FileReadUtil
from utils.LoggerUtil import logger
from utils.YamlUtil import YamlUtil

filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestSysLogin:

    def setup_method(self):
        LoginService().write_token()

    @pytest.mark.parametrize("datas", YamlUtil().get_testcases(filepath))
    def test_sys_login_success_01(self, datas: list):
        process_datas = []
        if isinstance(datas, dict):
            process_datas.append(datas)
        else:
            process_datas = datas
        for data in process_datas:
            ProcessCaseInfo().process_allure_info(data['allureInfo'])
            for req in data["requests"]:
                with allure.step(req["stepName"]):
                    res = ProcessCaseInfo().handle_case(req, FileReadUtil("./pytest.ini").read_conf("test"))
                    try:
                        if req["validate"] != None:
                            AssertUtil().assertion(req["validate"], res)
                        if req["extract"]!=None:
                            ExtractUtil().process_extract(req["extract"], res)
                    except Exception as e:
                        logger.error("用例缺位少关键字："+e.__str__())
