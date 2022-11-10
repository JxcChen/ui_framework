# -*- coding:utf-8 -*-
# @Time     :2022/7/30 4:06 下午
# @Author   :CHNJX
# @File     :shares_page.py
# @Desc     :股票页面
from selenium.webdriver.common.by import By

from mini_project.base.app import App


class SharesPage(App):
    def search(self, key):
        self.find_and_click((By.ID, 'action_search')).find_and_send(key, By.ID, 'search_input_text')
