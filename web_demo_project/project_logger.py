# -*- coding:utf-8 -*-
# @Time     :2022/8/1 16:10
# @Author   :CHNJX
# @File     :project_logger.py
# @Desc     :获取日志控制器  单利模式
from app_demo_project.base import LoggerHandler


def singleton(cls):
    # 创建一个字典用来保存类的实例对象
    _instance = {}

    def _singleton(*args, **kwargs):
        # 先判断这个类有没有对象
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)  # 创建一个对象,并保存到字典当中
        # 将实例对象返回
        return _instance[cls]

    return _singleton


class TestLogger:
    _logger = None

    # 静态变量
    _instance = None
    _flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._flag:
            self._flag = True
            self._logger = LoggerHandler.getLogger('test', 'app_demo.log', 'debug')

    def get_logger(self):
        return self._logger


l1 = TestLogger()
l2 = TestLogger()
l1.get_logger().info('test1')
l2.get_logger().info('test2')
