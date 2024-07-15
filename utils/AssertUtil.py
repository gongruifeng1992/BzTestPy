# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:AssertUtil.py
@data:2024/7/10 9:12 上午
"""
from common.ProcessCaseInfo import ProcessCaseInfo
from utils.ExtractUtil import ExtractUtil


class AssertUtil:
    def assertion(self, validate_list,res):
        """从yaml文件读取结果中获取validate"""
        for rule in validate_list:
            rule = dict(rule)
            for key in rule.keys():
                check_type = key
                rule_list = rule.get(key)
                process_list=[]
                for rule in rule_list:
                    if "${" and "}" in rule:
                        process_list.append(ProcessCaseInfo().process_data(rule))
                    elif "$." in rule:
                        process_list.append(ExtractUtil().process_extract(rule,res))
                    else:
                        process_list.append(rule)

                actual_value =process_list[0]
                expect_value =process_list[1]
                AssertUtil().validate_response(check_type, actual_value, expect_value)

    def validate_response(self, check_type, actual_value, expect_value):
        """根据获取类型，进行断言操作"""
        if check_type in ["eq", "equals", "equal"]:
            assert actual_value == expect_value
        elif check_type in ["lt", "less_than"]:
            assert actual_value < expect_value
        elif check_type in ["le", "less_or_equals"]:
            assert actual_value <= expect_value
        elif check_type in ["gt", "greater_than"]:
            assert actual_value > expect_value
        elif check_type in ["ne", "not_equal"]:
            assert actual_value != expect_value
        elif check_type in ["contains"]:
            assert actual_value in expect_value
        elif check_type in ["startswith"]:
            assert actual_value.startswith(expect_value)
        elif check_type in ["endswith"]:
            assert actual_value.endswith(expect_value)
        elif check_type in ["length"]:
            assert actual_value.__len__() == expect_value, actual_value + "length不等于" + expect_value
        elif check_type in ["exist"]:
            assert actual_value != "0000", "数据不存在！"
        else:
            print(f'{check_type}  not valid check type')
