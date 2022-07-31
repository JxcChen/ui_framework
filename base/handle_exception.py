# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:51 下午
# @Author   :CHNJX
# @File     :handle_exception.py
# @Desc     :处理异常弹框
import datetime

import allure
from selenium.webdriver.common.by import By

_black_list = [(By.XPATH, "//*[@resource-id='iv_close']"),
               (By.XPATH, "//*[text='下一步']"),
               (By.XPATH, "//*[text='等待']"),
               (By.XPATH, "//*[text='取消']"),
               (By.XPATH, "//*[text='等待']"),
               (By.XPATH, "//*[text='我知道了']"), ]
_max_time = 3


def handle_exception(func):
    def close_exception(*args, **kwargs):
        from base.base_page import BasePage
        # 获取实例  args[0] = self
        instance: BasePage = args[0]
        try:
            res = func(*args, **kwargs)
            instance.current_time = 0
            return res
        except Exception as e:
            if _max_time <= instance.current_time:
                raise e
            instance.current_time += 1
            # 查看是否存在黑名单内容  有则进行关闭
            for black in _black_list:
                ele = instance.find_elements(black)
                if ele:
                    ele[0].click()
                    # 进行递归
                    return close_exception(*args, **kwargs)
            # 截图
            instance.save_screenshot()
            raise e

    return close_exception
