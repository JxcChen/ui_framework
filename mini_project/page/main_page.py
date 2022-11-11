# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:20 下午
# @Author   :CHNJX
# @File     :main_page.py
# @Desc     :app主页
from time import sleep

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

from mini_project import project_logger
from mini_project.page.shares_page import SharesPage
from mini_project.base.app import App


class MainPage(App):
    def into_baoshi_page(self):
        """
        报事页面
        """
        self.find_and_click(MobileBy.XPATH, "//wx-button")

    def into_mini_main_page(self):
        """
        进入小程序首页
        :return: 当前页面
        """

        self.find_and_click(MobileBy.XPATH, "//*[@text='发现']") \
            .find_and_click(MobileBy.XPATH, "//*[@text='小程序']") \
            .find_and_click(MobileBy.XPATH, "//*[@text='想家友邻']")
        sleep(2)
        self.switch_context()
        self.switch_windows(':VISIBLE')
        return self
