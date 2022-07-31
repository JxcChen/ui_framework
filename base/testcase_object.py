# -*- coding:utf-8 -*-
# @Time     :2022/7/31 3:10 下午
# @Author   :CHNJX
# @File     :testcase_object.py
# @Desc     :测试用例的实体类
import importlib

from app_demo_project.page.page_generate import PageGenerate
from base import global_val
from base.utils import replace_form_2_actual


class Testcase:
    run_set_up_class_time = 0

    def __init__(self):
        self.set_up_class = []
        self.set_up = []
        self.ids = []
        self.steps_list = []
        self.data = []
        self.teardown = []
        self.teardown_class = []

    def run(self, test_steps):
        """执行用例"""
        # 先判断是否有set_up
        if self.set_up_class:
            if self.run_set_up_class_time == 0:
                # 确保只运行一次
                for set_up_class_step in self.set_up_class:
                    run_steps(set_up_class_step)
                self.run_set_up_class_time += 1
        if self.set_up:
            for set_up_step in self.set_up:
                self.run_steps(set_up_step)
        self.run_steps(test_steps)

    def run_steps(self,steps: list[dict]):
        """
        执行测试步骤
        :param steps:
        :return:
        """
        for step in steps:
            for (k, v) in step.items():
                k: str
                if k == 'data':
                    for (param_key,param_val) in v:
                        self.data[param_key] = param_val
                elif k == 'print':
                    print(v)
                elif '.' in k:
                    pg = PageGenerate()
                    page_method = k.split('.')
                    if v:
                        global_val.val_list.update(v)
                    pg.run_action(page_method[0], page_method[1])
                elif 'validate' in k:
                    # 进行断言处理
                    for assert_content in v:
                        for (assert_method, assert_value) in assert_content.items():
                            expect_value = assert_value[0]
                            run_value = assert_value[1]
                            if '$' in run_value:
                                run_value = replace_form_2_actual(run_value, global_val.save_list)
                            if assert_method == 'in':
                                if type(run_value) is list:
                                    assert expect_value in run_value
                                if type(run_value) is str:
                                    assert expect_value in run_value
                            elif assert_method == 'equals':
                                assert expect_value == run_value

