# -*- coding:utf-8 -*-
# @Time     :2022/7/30 5:32 下午
# @Author   :CHNJX
# @File     :test_yaml.py
# @Desc     :
from web_demo_project.page.page_generate import PageGenerate
page = PageGenerate()

def test_yaml_load():
    page.generate_page('main_page')

def test_run_method():
    page.run_action('main_page','search_keyword')
    page.run_action('search_page', 'get_search_result_list')
    print('debug')


