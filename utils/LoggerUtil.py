# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:LoggerUtil.py
@data:2024/7/4 2:47 下午
"""
import logging
import os.path
import time

import colorlog

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_path = os.path.join(root_path, "../BzTestPy/log")


class LoggerUtil:
    def __init__(self):
        # 定义日志位置和文件名
        self.logname = os.path.join(log_path, "{}.log".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        # 定义一个日志容器
        self.logger = logging.getLogger("logger")
        # 设置日志打印的级别
        self.logger.setLevel(logging.DEBUG)
        # 创建日志输入的格式
        self.formatter = colorlog.ColoredFormatter('%(asctime)s - %(filename)s-%(levelname)s - %(message)s',
                                                   datefmt=None,
                                                   reset=True,
                                                   log_colors={
                                                       'DEBUG': 'cyan',
                                                       'INFO': 'green',
                                                       'WARNING': 'yellow',
                                                       'ERROR': 'red',
                                                       'CRITICAL': 'red,bg_white'
                                                   }, secondary_log_colors={}, style='%'
                                                   )
        # 创建日志处理器，用来存放日志文件
        self.filelogger = logging.FileHandler(self.logname, mode='a', encoding='utf-8')
        # 创建日志处理器，在控制台打印
        self.console = logging.StreamHandler()
        # 设置控制台打印日志级别
        self.console.setLevel(logging.DEBUG)
        # 设置文件存放日志级别
        self.filelogger.setLevel(logging.DEBUG)
        # 文件存放日志格式
        self.filelogger.setFormatter(self.formatter)
        # 控制台打印日志格式
        self.console.setFormatter(self.formatter)
        # 将日志输出渠道添加到日志收集器中
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)


logger = LoggerUtil().logger


