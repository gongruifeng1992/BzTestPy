# !/usr/bin/env python
# -*- coding: UTF-8 _*_
"""
@project:BzTestPy
@author:张美丽
@file:confest.py.py
@data:2024/7/4 1:59 下午
"""
import configparser

import pytest

from utils.FileReadUtil import FileReadUtil
from utils.LoggerUtil import logger

settings_path="/Users/jijia/PycharmProjects/BzTestPy/settings.ini"

def pytest_addoption(parser):
    parser.addoption(
            "--env",
            action="store",
            dest="enviroment",
            default="test",
            help="test：测试环境"
                 "tenant：租户环境"
                 "product：生产环境"
        )
    logger.info("设置多环境参数env:"+str(parser.addoption))



@pytest.fixture(scope="session",autouse=True)
def env(pytestconfig):
    return pytestconfig.getoption("enviroment")

@pytest.fixture(scope="session",autouse=True)
def get_env(env):
    """从配置对象中获取自定义参数的值"""
    try:
        if (env == "test"):
            return FileReadUtil(settings_path).read_conf("test")
        elif (env == "tenant"):
            return FileReadUtil(settings_path).read_conf("tenant")
        elif (env == "prod"):
            return FileReadUtil(settings_path).read_conf("prod")
        else:
            logger.error("输入环境参数错误！【test tenant prod】")
    except:
        logger.error("获取环境参数异常！")


def write_envir(section_name):
    conf = configparser.ConfigParser()
    conf.add_section(section_name)
    source_data = FileReadUtil("settings.ini").read_conf(section_name)
    for key, value in source_data.items():
        conf.set(section_name, key, value)
    FileReadUtil("pytest.ini").write_conf(conf, "a")

def delete_envir(section_name):
    source_data = FileReadUtil("pytest.ini").read_conf_all()
    source_data.remove_section(section_name)
    return source_data


@pytest.fixture(scope="session",autouse=True)
def set_env(get_env):
    """
    将自定义参数值些人全局配置文件中
    :param get_env:
    :return:
    """
    section_name=get_env.name
    try:
        data=FileReadUtil("pytest.ini").read_conf(section_name)
    except:
        data=None

    if data==None:
        logger.info("section:"+section_name+"不存在，直接写入")
        write_envir(section_name)
    else:
        logger.info("section:"+section_name+"已存在，将删除后新增")

        delete_data=delete_envir(section_name)
        FileReadUtil("pytest.ini").write_conf(delete_data, "w")
        write_envir(section_name)


@pytest.fixture(scope="function",autouse=True)
def empty_extract():
    yield
    FileReadUtil("./extract.yaml").delete_yaml_all()

# @pytest.fixture(scope="session",autouse=True)
# def empty_ini():
#     conf=FileReadUtil("./pytest.ini").read_conf_all()
#     FileReadUtil("./pytest.ini").delet_conf(conf,"test")
#     FileReadUtil("./pytest.ini").write_conf(conf,"w")

