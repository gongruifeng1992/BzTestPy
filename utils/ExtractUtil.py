# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:ExtractUtil.py
@data:2024/7/10 11:13 上午
"""
import jsonpath

from utils.LoggerUtil import logger


class ExtractUtil:
    def process_extract(self, extract:str, res: dict):

        if extract != None:
            try:
                extract_res = jsonpath.jsonpath(res, extract)
                if extract_res.__len__()==1:
                    return extract_res[0]
                else:
                    return extract_res
            except:
                return '0000'
                logger.error("jsonpath没有获取到数据："+extract)
        else:
            logger.error("extract返回格式错误，无法提取数据！")
