# @Time     :2022/7/30 5:22 下午
# @Author   :CHNJX
# @File     :app_page_generate.py
# @Desc     :将yaml转换成页面
import logging
import os
import time

import yaml

from web_demo_project.testcase.utils import Utils
from web_demo_project.base.web import Web
from web_demo_project.base import global_val


class PageGenerate(Web):
    page_list = {}
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    res = None

    def generate_page(self, page_name: str):
        # 获取yaml中的页面并进行储存
        if not self.page_list.get(page_name):
            with open(f'{os.path.dirname(__file__)}/{page_name}.yml', encoding='utf-8') as page:
                cur_page = yaml.safe_load(page)
            for (key, value) in cur_page.items():
                self.page_list[key] = value
                # 打开首页
                # if value.get('init'):
                #     for init_step in value.get('init'):
                #         self.driver.get(init_step['get'])
            # action = self.page_list.get(page_name)['actions']
        return self.page_list.get(page_name)['actions']

    def run_action(self, page_name, action_name: str):
        # 先对页面进行转换
        actions = self.generate_page(page_name)
        if not actions.get(action_name):
            logging.error('当前页面不存在' + action_name + '方法')
            return
        for step in actions[action_name]:
            for (key, value) in step.items():
                if key == 'get':
                    self.driver.get(value)
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
