# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:21 下午
# @Author   :CHNJX
# @File     :test_demo.py
# @Desc     :app测试用例
from mini_project.base.app import App
from mini_project.page.main_page import MainPage


class TestDemo:
    def setup_class(self):
        self.main = MainPage().init_mini_main_page()

    def test_report_home_repair(self):
        assert '提交成功' in self.main.into_report_page().report_home_repair().get_report_result()

