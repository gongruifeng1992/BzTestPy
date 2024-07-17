# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:process_case_info_util.py
@data:2024/7/4 3:50 下午
"""
import importlib
import re

import allure

from utils.FileReadUtil import FileReadUtil
from utils.LoggerUtil import logger
from utils.RequestUtil import RequestUtil


class ProcessCaseInfo:

    def process_allure_info(self, data):
        """
        allure报告赋值
        :param data:
        :return:
        """
        try:
            allure.dynamic.epic(data["epic"])
            allure.dynamic.feature(data["feature"])
            allure.dynamic.description(data["description"])
            allure.dynamic.story(data["story"])
            allure.dynamic.title(data["title"])
        except Exception as e:
            logger.error("allure信息注入失败，缺少字段：" + e.__str__())

    def process_data(self, data1):
        """
        将字符串中的函数替换为对应字符串
        :param data:
        :return:
        """
        if data1 is None:
            data = ""
        data=str(data1)
        if "${" and "}" in data:
            for i in range(data.count("${")):
                if re.match("(.*)\${(.*)",data):
                    start_index = data.index("${")
                    end_index = data.index("}")

                    func_full_name = data[start_index + 2:end_index]
                    names = func_full_name.split(").")
                    func_name = names[1][:names[1].index('(')]
                    names[0] = names[0] + ")"
                    module_params = names[0][names[0].index("(") + 1:names[0].index(")")]
                    func_params = names[1][names[1].index('(') + 1: names[1].index(')')]
                    module_names = re.split('(?<!^)(?=[A-Z])', names[0][:names[0].index("(")])
                    module_name = ""
                    for i in range(len(module_names)):
                        module_name = module_name + module_names[i]
                    if "Util" in module_name:
                        moudule_path = "utils." + module_name
                    else:
                        moudule_path = "common." + module_name
                    if module_params != '':
                        extract_data = getattr(importlib.import_module(moudule_path), module_name, None)(module_params)
                    else:
                        extract_data = getattr(importlib.import_module(moudule_path), module_name, None)()
                    if extract_data is not None:
                        if func_params != '':
                            param_list = func_params.split(",")
                            extract_param = []
                            for para in param_list:
                                if "Util" in module_name:
                                    return FileReadUtil("./extract.yaml").read_yaml()[
                                        para]
                                else:
                                    extract_param.append(
                                        FileReadUtil("./extract.yaml").read_yaml()[
                                            para])

                            if "Util" in module_name:
                                return extract_param
                            elif extract_param != "":
                                reslut = getattr(extract_data, func_name, None)(*extract_param)
                                final_data = data.replace(data[start_index: end_index + 1], reslut)
                                return str(final_data)
                        else:
                            reslut = getattr(extract_data, func_name, None)()
                            final_data = data.replace(data[start_index: end_index + 1], str(reslut))
                            return str(final_data)

        else:
            return data1

    def process_headers(self, token, content_type="application/json"):
        """
        组装headers
        :param token:
        :param content_type:
        :return:
        """
        conf=FileReadUtil("pytest.ini").read_conf("test")["token"]
        headers = {
            "referer": "https://servicewechat.com/wxa85ba67d8885ce5f/0/page-frame.html",
            "charset": "utf-8",
            "x-request-token": conf ,
            "User-Agent": "[{\"key\":\"User-Agent\",\"value\":\"Mozilla/5.0 (Linux; Android 12; SM-N9860 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220903 Mobile Safari/537.36 MMWEBID/9048 MicroMessenger/8.0.28.2240(0x28001C35) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android\",\"enabled\":true}]",
            "content-type": content_type,
            "accept": "application/json, text/plain, */*"
        }

        return headers

    def handle_case(self, step: dict,conf):
        stepName = step.pop("stepName")
        url = conf['host'] + self.process_data(step.pop("url"))
        method = step.pop("method").lower()
        headers = self.process_headers(step.pop("headers"))
        validate = step.pop("validate")
        try:
            extract = step.pop("extract")
        except:
            pass
        process_body = {}
        para_type=""
        if step != {}:
            for key in step.keys():
                para_type=key
                for keyname in step[key]:
                    res = ProcessCaseInfo().process_data(step[key][keyname])
                    process_body[keyname] = res
            param={para_type:process_body}
            res = RequestUtil().sendRequest(url=url, headers=headers, method=method,**param)
        else:
            res = RequestUtil().sendRequest(url=url, headers=headers, method=method)
        try:
            step["validate"] = validate
            step["extract"] = extract
            step["stepName"] = stepName
        except:
            pass
        return res

    def get_status_code(self, res):
        return str(res.status_code)
if __name__ == '__main__':
    source="${loh.wfre(${cdsv.desf())}"
    print(re.match("(.*)\${(.*)",source))