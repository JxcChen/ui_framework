# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:58 下午
# @Author   :CHNJX
# @File     :test_yaml.py
# @Desc     :
from mini_project.page.app_page_generate import PageGenerate


def test_01():
    page = PageGenerate()
    page.run_action('main_page','into_shares_page')
    page.run_action('shares_page', 'search')
