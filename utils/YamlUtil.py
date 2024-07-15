# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:YamlUtil.py
@data:2024/7/12 5:44 下午
"""
import glob
import os

import yaml

from utils.LoggerUtil import logger


class YamlUtil:

    def get_file_paths(self, path, list_name: list):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                YamlUtil().get_file_paths(file_path, list_name)
            elif ".yaml" in file_path:
                list_name.append(file_path)
        return list_name

    def combine_yaml(self, filepath_list):
        testcase_list = []
        try:
            for filepath in filepath_list:
                with open(filepath, "r") as file:
                    data = yaml.safe_load(file)
                    testcase_list += data
        except Exception as e:
            logger.error("用例数据文件不能为空！")

        return testcase_list

    def get_testcases(self, folder_path):
        filepath_list = []
        path_list = YamlUtil().get_file_paths(folder_path, filepath_list)
        testcase_list = YamlUtil().combine_yaml(path_list)
        return testcase_list


if __name__ == '__main__':
    print(YamlUtil().get_testcases("../testcase/data"))
