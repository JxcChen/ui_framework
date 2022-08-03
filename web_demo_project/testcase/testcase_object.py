# -*- coding:utf-8 -*-
# @Time     :2022/7/31 3:10 下午
# @Author   :CHNJX
# @File     :testcase_object.py
# @Desc     :测试用例的实体类

from web_demo_project.page.web_page_generate import PageGenerate
from web_demo_project.base import global_val
from web_demo_project.testcase.utils import Utils


class Testcase:
    run_set_up_class_time = 0

    def __init__(self):
        self.set_up_class = []
        self.set_up = []
        self.ids = []
        self.steps_list = []
        self.data = {}
        self.teardown = []
        self.teardown_class = []

    def run(self, test_steps):
        """执行用例"""
        # 先判断是否有set_up
        if self.set_up_class:
            if self.run_set_up_class_time == 0:
                # 确保只运行一次
                for set_up_class_step in self.set_up_class:
                    self.run_steps(set_up_class_step)
                self.run_set_up_class_time += 1
        if self.set_up:
            for set_up_step in self.set_up:
                self.run_steps(set_up_step)
        self.run_steps(test_steps)

    def run_steps(self, steps: list[dict]):
        """
        执行测试步骤
        :param steps: 步骤
        :return:
        """
        pg = PageGenerate()
        for step in steps:
            for (k, v) in step.items():
                k: str
                if k == 'print':
                    print(v)
                elif '.' in k:
                    page_method = k.split('.')
                    if v:
                        run_value = Utils.resolve_dict(v,global_val.actual_list)
                        global_val.val_list.update(run_value)
                    pg.run_action(page_method[0], page_method[1])
                elif 'validate' in k:
                    # 进行断言处理
                    for assert_content in v:
                        for (assert_method, assert_value) in assert_content.items():
                            expect_value = assert_value[0]
                            run_value = assert_value[1]
                            if '$' in run_value:
                                run_value = Utils.replace_form_2_actual(run_value, global_val.save_list)
                            if '$' in expect_value:
                                expect_value = Utils.replace_form_2_actual(expect_value, global_val.actual_list)
                            if assert_method == 'in':
                                if type(run_value) is list:
                                    assert expect_value in run_value
                                if type(run_value) is str:
                                    assert expect_value in run_value
                            elif assert_method == 'equals':
                                assert expect_value == run_value


