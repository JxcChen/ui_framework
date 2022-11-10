# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:21 下午
# @Author   :CHNJX
# @File     :test_demo.py
# @Desc     :app测试用例
from mini_project.base.app import App
from mini_project.page.main_page import MainPage


class TestDemo:
    def setup_class(self):
        self.main = MainPage().into_mini_main_page()

    def test_02(self):
        self.main.into_baoshi_page()
