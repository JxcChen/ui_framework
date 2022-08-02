# -*- coding:utf-8 -*-
# @Time     :2022/8/1 15:50
# @Author   :CHNJX
# @File     :project_logger.py
# @Desc     :測試日志
from app_demo_project.base import LoggerHandler

logger = LoggerHandler.get_logger('testcase', 'app_demo_log')


def test_logger():
    logger.info('test logger')
