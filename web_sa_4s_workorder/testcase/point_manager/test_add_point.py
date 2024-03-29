# -*- coding:utf-8 -*-
# @Time     :2022/7/31 10:51 上午
# @Author   :CHNJX
# @File     :test_search2.py
# @Desc     :搜素用例
import os

import pytest

from web_sa_4s_workorder.testcase.testcase_generate import TestcaseGenerate

steps = {}


class TestCase:
    tg = TestcaseGenerate()
    tg.load_case(os.path.dirname(__file__)+'/'+str(__name__).split('.')[-1] + '.yml')

    @pytest.mark.parametrize(
        'testcase',
        tg.testcase.steps_list,
        ids=tg.testcase.ids
    )
    def test_param(self, testcase):
        self.tg.run_case(testcase)
