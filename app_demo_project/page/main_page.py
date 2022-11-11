# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:20 下午
# @Author   :CHNJX
# @File     :main_page.py
# @Desc     :app主页
from selenium.webdriver.common.by import By

from app_demo_project import project_logger
from app_demo_project.page.shares_page import SharesPage
from app_demo_project.base.app import App


class MainPage(App):
    def into_shares_page(self):
        """
        进入股票页面
        """
        self.find_and_click((By.XPATH, "//*[text='股票']"))
        return SharesPage(self.driver)
