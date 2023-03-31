# -*- coding:utf-8 -*-
# @Time     :2022/8/1 16:10
# @Author   :CHNJX
# @File     :project_logger.py
# @Desc     :获取日志控制器  单例模式
from web_demo_project_bak.base.logger_handler import LoggerHandler


class ProjectLogger:
    _logger = None
    _instance = None
    _flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._flag:
            self._flag = True
            self._logger = LoggerHandler.get_logger('test', 'web_demo.log', 'debug')

    def get_logger(self) -> object:
        return self._logger
