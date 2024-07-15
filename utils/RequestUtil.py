# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:RequestUtil.py
@data:2024/7/4 5:48 下午
"""
import json
import threading

import requests as requests

from utils.LoggerUtil import logger


class RequestUtil:
    sess = requests.session()

    def sendRequest(self, **kwargs):
        """
        发送请求
        :param kwargs:
        :return: res
        """
        res = RequestUtil.sess.request(**kwargs)
        threadName = threading.currentThread().name
        logger.info("-----------------" + threadName + "--------------------")
        logger.info("url:  "+res.url)
        logger.info("headers:  "+res.request.headers.__str__())
        logger.info("body: "+str(res.request.body))
        logger.info("status_code:  "+res.status_code.__str__())
        logger.info("res.text:  "+res.text.__str__())
        logger.info("--------------------请求结束---------------------------")

        if res.text.startswith("{"):
            response={"status_code":str(res.status_code),
                "text":json.loads(res.text)}
            return response
        else:
            response = {"status_code": str(res.status_code),
                        "text": str(res.text)}
            return response