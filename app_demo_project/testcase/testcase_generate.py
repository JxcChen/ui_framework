# -*- coding:utf-8 -*-
# @Time     :2022/7/31 2:36 下午
# @Author   :CHNJX
# @File     :testcase_generate.py
# @Desc     :动态生成用例
import os

import yaml

from base.testcase_object import Testcase


class TestcaseGenerate:

    def __init__(self):
        self.testcase = Testcase()
        self.data = None

    def load_case(self, file_path):
        with open(os.path.dirname(__file__) + '/' + file_path) as f:
            self.data = yaml.safe_load(f)
        self.generate()

    def generate(self):
        for (title, steps) in self.data.items():
            if title == 'set_up':
                self.testcase.set_up.append(steps)
            elif title == 'set_up_class':
                self.testcase.set_up_class.append(steps)
            if title == 'teardown':
                self.testcase.teardown.append(steps)
            elif title == 'teardown_class':
                self.testcase.teardown_class.append(steps)
            elif str(title).startswith('test'):
                self.testcase.ids.append(title)
                self.testcase.steps_list.append(steps)

    def run_case(self, test_steps: list):
        self.testcase.run(test_steps)


