# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:28 上午
# @Author   :CHNJX
# @File     :main_page.py
# @Desc     :demo主页
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from demo_project.page.search_page import SearchPage

INDEX_URL = "https://www.baidu.com"

from base.web import Web




class MainPage(Web):
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
        self.driver.get(INDEX_URL)

    def search_keyword(self, kw):
        """
        搜索关键字
        :param kw: 关键字
        :return: list
        """
        self.find_and_send(kw, By.ID, 'kw').wait_for_click((By.ID, 'su')).click()
        time.sleep(2)
        return SearchPage(self.driver)

