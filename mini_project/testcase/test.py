# -*- coding:utf-8 -*-
# @Time     :2022/7/31 3:37 下午
# @Author   :CHNJX
# @File     :test.py
# @Desc     :
import importlib

i = importlib.import_module('app_demo_project.page.page_generate')

getattr(i, 'test')()
