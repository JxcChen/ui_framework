# -*- coding:utf-8 -*-
# @Time     :2022/7/31 2:36 下午
# @Author   :CHNJX
# @File     :testcase_generate.py
# @Desc     :动态生成用例
import os

import yaml

from web_demo_project import project_logger
from web_demo_project.base import global_val
from web_demo_project.testcase.testcase_object import Testcase


class TestcaseGenerate:

    def __init__(self):
        self.testcase = Testcase()
        self.data = None
        self.logger = project_logger.ProjectLogger().get_logger()

    def load_case(self, file_path):
        with open(os.path.dirname(__file__) + '/' + file_path) as f:
            self.data = yaml.safe_load(f)
        self.generate()

    def generate(self):
        for (title, steps) in self.data.items():
            if title == 'set_up':
                self.testcase.set_up.append(steps)
            elif title == 'data':
                self.testcase.data = steps
            elif title == 'set_up_class':
                self.testcase.set_up_class.append(steps)
            if title == 'teardown':
                self.testcase.teardown.append(steps)
            elif title == 'teardown_class':
                self.testcase.teardown_class.append(steps)
            elif str(title).startswith('test'):
                self.testcase.ids.append(title)
                self.testcase.steps_list.append({title: steps})

    def run_case(self, test_steps: dict):
        current_index = 0
        val_len = None
        for (i, v) in test_steps.items():
            # 参数化驱动

            if self.testcase.data.get(i):
                data_dict: dict = self.testcase.data[i]
                while val_len is None or current_index < val_len:
                    for (keys, values) in data_dict.items():
                        self.logger.info(f'测试用例 - {i}   当前参数：{values[current_index]}')
                        val_len = len(values)
                        if current_index < len(values):
                            global_val.actual_list[keys] = values[current_index]

                    current_index += 1
                    self.testcase.run(v)
            else:
                self.testcase.run(v)
