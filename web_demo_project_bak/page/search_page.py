# -*- coding:utf-8 -*-
# @Time     :2022/7/30 11:13 上午
# @Author   :CHNJX
# @File     :search_page.py
# @Desc     :搜索后的结果页面
from selenium.webdriver.common.by import By

from web_demo_project_bak.base.web import Web


class SearchPage(Web):
    def get_search_result_list(self):
        """
        返回
        :return: 响应结果列表
        """
        res = [ele.text for ele in self.find_elements(By.XPATH, "//h3/a/em")]
        return [ele.text.lower() for ele in self.find_elements(By.XPATH, "//h3/a/em")]


