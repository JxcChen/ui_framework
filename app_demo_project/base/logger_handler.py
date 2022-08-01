# -*- coding:utf-8 -*-
# @Time     :2022/8/1 15:12
# @Author   :CHNJX
# @File     :logger_handler.py
# @Desc     :日志收集器
import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler


class LoggerHandler:
    workdir = os.path.split(os.path.realpath(__file__))[0]

    @classmethod
    def getLogger(cls, name, package_name,log_level='debug'):
        """
        获取日志控制器
        :param name: 日至控制器名称
        :param package_name: 存放的包名
        :param log_level: 日志收集等级 默认为debug
        """
        logger = logging.getLogger(name)
        if log_level == 'debug':
            logger.setLevel(logging.DEBUG)
        elif log_level == 'info':
            logger.setLevel(logging.INFO)
        elif log_level == 'error':
            logger.setLevel(logging.ERROR)
        time_format = '%Y%m%d'
        now_string = time.strftime(time_format, time.localtime(time.time()))
        file_name = 'log_{}.log'.format(now_string)
        root_path = os.path.abspath(
            os.path.join(cls.workdir, "../logs"))
        _folder_path = os.path.join(root_path, package_name)
        if not os.path.exists(_folder_path):
            os.mkdir(_folder_path)
        file_path = os.path.join(_folder_path, file_name)
        t = int(time.time())
        if TimedRotatingFileHandler(file_path).when.startswith('D') and time.localtime(t).tm_mday == time.localtime(
                TimedRotatingFileHandler(file_path).rolloverAt).tm_mday:
            return 1
        else:
            pass

        # FileHandler
        fh = logging.FileHandler(file_path, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '******%(asctime)s - %(name)s - %(filename)s,line %(lineno)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.addHandler(sh)
        # logger.addHandler(uh)

        return logger
