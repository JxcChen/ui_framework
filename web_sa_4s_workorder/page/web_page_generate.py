# @Time     :2022/7/30 5:22 下午
# @Author   :CHNJX
# @File     :web_page_generate.py
# @Desc     :将yaml转换成页面
import importlib
import logging
import os
import platform
import time

import yaml

from web_sa_4s_workorder.base.utils import Utils
from web_sa_4s_workorder.base.web import Web
from web_sa_4s_workorder.base import global_val, utils


class PageGenerate(Web):
    page_list = {}
    res = None

    def generate_page(self, page_name: str):
        """
        获取yaml中的页面并进行储存
        :param page_name: 页面名称
        """
        if not self.page_list.get(page_name):
            # 先获取文件路径
            file_path = utils.Utils.search_file(os.path.dirname(__file__),f'{page_name}.yml')
            with open(file_path,encoding='utf-8') as page:
                cur_page = yaml.safe_load(page)
            for (key, value) in cur_page.items():
                self.page_list[key] = value
        # if not self.page_list.get(page_name):
        #     with open(f'{os.path.dirname(__file__)}/{page_name}.yml', encoding='utf-8') as page:
        #         cur_page = yaml.safe_load(page)
        #     for (key, value) in cur_page.items():
        #         self.page_list[key] = value
        return self.page_list.get(page_name)['actions']

    def run_action(self, page_name, action_name: str):
        """
        调用对应页面方法方法
        :param page_name: 页面名称
        :param action_name: 方法名称
        """
        # 先对页面进行转换
        actions = self.generate_page(page_name)
        if not actions.get(action_name):
            logging.error('当前页面不存在' + action_name + '方法')
            return
        self.run(actions[action_name])

    def run(self, action: list[dict]):
        """
        执行具体的action步骤
        :param action: 步骤列表  type：list[dict]
        """
        for step in action:
            for (key, value) in step.items():
                key: str
                run_value = value
                if key.startswith('if'):
                    # 如果有if说明是选填项  判断用户是否有传值
                    # 如果没有传值则不执行
                    run_key = key[3:]
                    if run_key in global_val.val_list.keys():
                        self.run(run_value)
                elif key == 'get':
                    self.driver.get(run_value)
                elif key == 'find':
                    from selenium.webdriver.common.by import By
                    by = value[0]
                    if value[0] == 'css':
                        by = By.CSS_SELECTOR

                    locator = value[1]
                    if '${' in locator:
                        locator = Utils.replace_form_2_actual(locator, global_val.val_list)

                    self.find_element(by, locator)
                elif key == 'send':
                    if '${' in str(run_value):
                        run_value = Utils.replace_form_2_actual(run_value, global_val.val_list)
                    self.send(run_value)
                elif key == 'click':
                    self.click()
                elif key == 'return':
                    if 'page' in value:
                        self.generate_page(run_value)
                elif key == 'find_elements':
                    if '${' in run_value:
                        run_value = Utils.replace_form_2_actual(run_value, global_val.val_list)
                    if len(run_value) == 3:
                        self.find_elements(run_value[0], run_value[1], run_value[2])
                    else:
                        self.find_elements(run_value[0], run_value[1])
                elif key == 'get_elements_text':
                    self.res = self.get_elements_text()
                elif key == 'text':
                    self.res = self.get_element_text()
                elif key == 'save':
                    # 存储上一步返回的变量
                    global_val.save_list[run_value] = self.res
                elif key == 'sleep':
                    time.sleep(run_value)
                elif '.' in key:
                    module_method = key.split('.')
                    # 导入包  如果系统包中没有则需要导入自己的包
                    # 自己的包默认放在项目路径下
                    try:
                        module = importlib.import_module("token_helper")
                    except Exception as e:
                        pro_path = os.path.dirname(os.path.dirname(__file__))
                        # 需要根据不同系统做不同操作
                        if platform.system() == 'Windows':
                            project_package = pro_path.split("\\")[-1]
                        else:
                            project_package = pro_path.split("/")[-1]
                        module = importlib.import_module(f"{project_package}.token_helper")
                    r = getattr(module, module_method[1])()
                    if type(r) is str:
                        self.res = r
                elif 'js' in key:
                    # 执行js脚本
                    if '${' in run_value:
                        run_value = Utils.replace_form_2_actual(run_value, global_val.save_list)
                    self.driver.execute_script(run_value)
                elif 'refresh' == key:
                    # 刷新页面
                    self.driver.refresh()
                elif 'quit' == key or 'close' == key or 'teardown' == quit():
                    # 刷新页面
                    self.driver.close()
                elif 'quit' == key or 'teardown' == quit():
                    # 刷新页面
                    self.driver.quit()
