# -*- coding:utf-8 -*-
# @Time     :2022/7/30 5:22 下午
# @Author   :CHNJX
# @File     :page_generate.py
# @Desc     :将yaml转换成页面
import logging
import os
import time

import yaml

from app_demo_project import project_logger
from app_demo_project.base.app import App
from app_demo_project.base import global_val
from app_demo_project.base.utils import Utils


class PageGenerate(App):
    page_list = {}
    res = None

    def generate_page(self, page_name: str) -> dict:
        """
        读取文件并将页面和页面对应的方法进行储存 并范围对应的方法
        :param page_name: 页面名称
        :return:
        """
        # 获取yaml中的页面并进行储存
        if not self.page_list.get(page_name):
            with open(f'{os.path.dirname(__file__)}/{page_name}.yml', encoding='utf-8') as page:
                cur_page = yaml.safe_load(page)
            for (key, value) in cur_page.items():
                self.page_list[key] = value
                # 打开首页
                if value.get('init'):
                    for init_step in value.get('init'):
                        self.driver.get(init_step['get'])
        return self.page_list.get(page_name)['actions']

    def run_action(self, page_name:str, action_name: str):
        """
        执行页面对应的方法
        :param page_name:   页面名称
        :param action_name: 页面方法
        """
        # 先对页面进行转换
        actions = self.generate_page(page_name)
        if not actions.get(action_name):
            logging.error('当前页面不存在' + action_name + '方法')
            return
        for step in actions[action_name]:
            for (key, value) in step.items():
                if key == 'find':
                    self.find_element(value[0], value[1])
                elif key == 'send':
                    if '$' in str(value):
                        run_value = Utils.replace_form_2_actual(value, global_val.val_list)
                    else:
                        run_value = value
                    self.send(run_value)
                elif key == 'click':
                    self.click()
                elif key == 'return':
                    if 'page' in value:
                        self.generate_page(value)
                    else:
                        pass
                elif key == 'find_elements':
                    if len(value) == 3:
                        self.find_elements(value[0], value[1], value[2])
                    else:
                        self.find_elements(value[0], value[1])
                elif key == 'get_elements_text':
                    self.res = self.get_elements_text()
                elif key == 'text':
                    self.res = self.get_element_text()
                elif key == 'save':
                    global_val.save_list[value] = self.res
                elif key == 'sleep':
                    time.sleep(value)
                elif key == 'back':
                    self.back_to_main(value[0], value[1])
