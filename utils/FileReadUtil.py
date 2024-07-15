# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:FileReadUtil.py
@data:2024/7/4 2:38 下午
"""
import configparser

import yaml

from utils.LoggerUtil import logger


class FileReadUtil:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_yaml(self):
        """yaml文件读"""
        try:
            with open(self.filepath, encoding="utf-8", mode="r") as f:
                data = yaml.load(f, yaml.FullLoader)
                return data
        except Exception as e:
            logger.error("文件读写异常:", self.filepath)

    def read_yaml_key(self, key):
        try:
            with open(self.filepath, encoding="utf-8", mode="r") as f:
                data = yaml.load(f, yaml.FullLoader)
                return data[key]
        except Exception as e:
            logger.error("文件读写异常:", self.filepath)

    def write_yaml(self, data, type):
        with open(self.filepath, type, encoding='utf-8') as yaml_file:
            yaml.dump(data, yaml_file)

    def delete_yaml_all(self):
        with open(self.filepath, 'w', encoding='utf-8') as yaml_file:
            yaml_file.truncate()

    def read_conf(self, section):
        """
        读取配置文件，获取指定的section
        :return:
        """
        conf = configparser.ConfigParser()
        conf.read(self.filepath, encoding="utf8")
        return conf[section]


    def read_conf_all(self):
        """
        读取配置文件，返回整个conf
        :return:
        """
        try:
            conf = configparser.ConfigParser()
            conf.read(self.filepath, encoding="utf8")
            return conf
        except:
            pass


    def write_conf(self, conf, opertype):
        with open(self.filepath, encoding="utf-8", mode=opertype) as f:
            conf.write(f)


    def delet_conf(self, conf, section_name):
        conf.remove_section(section_name)


    def exist_key_yaml(self, data: dict):
        source_data = FileReadUtil(self.filepath).read_yaml()
        if source_data is not None:
            for key in data.keys():
                try:
                    source_data.pop(key)
                    source_data[key] = data.get(key)
                    FileReadUtil(self.filepath).write_yaml(source_data, "w")
                except:
                    source_data[key] = data.get(key)
                    FileReadUtil(self.filepath).write_yaml(source_data, "w")
        else:
            FileReadUtil(self.filepath).write_yaml(data, "w")


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("/Users/jijia/PycharmProjects/BzTestPy/settings.ini", encoding="utf8")
    print(conf.sections())
