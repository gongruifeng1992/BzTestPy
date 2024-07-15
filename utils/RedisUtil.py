# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:RedisUtil.py
@data:2024/7/8 10:43 上午
"""
import redis as redis

from utils.FileReadUtil import FileReadUtil

conf=FileReadUtil("./pytest.ini").read_conf("test")


class RedisUtil:
    def create_conn(self):
        conn = redis.Redis(conf["redis_host"], port=conf["redis_port"], decode_responses=True, username="",
                           password=conf["redis_password"])
        return conn

    def set_value(self, **datas):
        """
        key，value写入redis,支持批量写入
        :param datas:
        :return:
        """
        conn = RedisUtil().create_conn(conf)
        for key, value in datas.items():
            conn.set(key, value)

    def get_value(self, key_name):
        """
        根据key名获取值
        :param key_name:
        :return:
        """
        conn = RedisUtil().create_conn()
        res = conn.get(key_name)
        return res

    def delete_value(self, key_name):
        """
        根据key删除值
        :param key_name:
        :return:
        """
        conn = RedisUtil().create_conn(conf)
        res = conn.delete(key_name)
        return res

    def close_conn(self, conn):
        """
        关闭redis链接
        :param conn:
        :return:
        """
        conn.disconnect()
