# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:38 上午
# @Author   :CHNJX
# @File     :test_demo.py
# @Desc     :框架测试
import pytest

from web_sa_4s_workorder.page.main_page import MainPage


class TestDemo:
    main = MainPage()

    def test_01(self):
        print('test')

    def test_search(self):
        for text in self.main.search_keyword('selenium').get_search_result_list():
            assert 'selenium' == text

    def teardown_class(self):
        self.main.teardown()


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
