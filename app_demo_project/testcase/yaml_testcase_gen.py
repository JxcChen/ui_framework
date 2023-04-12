# -*- coding:utf-8 -*-
# @Time     :2023/4/12 18:12
# @Author   :CHNJX
# @File     :yaml_testcase_gen.py
# @Desc     :根据yaml文件生成用例


def gen_test(yaml_dir: str):
    # 需要根据yaml文件生成对应py文件
    py_test_demo = f"""
import os

import pytest

from mini_project.testcase.testcase_generate import TestcaseGenerate


class TestCase:
    tg = TestcaseGenerate()
    tg.load_case(r'{yaml_dir}')

    @pytest.mark.parametrize(
        'testcase',
        tg.testcase.steps_list,
        ids=tg.testcase.ids
    )
    def test_param(self, testcase):
        self.tg.run_case(testcase)
    """
    if '/' in yaml_dir:
        dir_list = yaml_dir.split('/')
    else:
        dir_list = yaml_dir.split('\\')
    dir_list[-1] = dir_list[-1].split('.')[0] + '.py'
    py_file = '/'.join(dir_list)
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write(py_test_demo)


gen_test(r'G:\pythonProject\ui_framework\app_demo_project\testcase\test_search.yml')