# -*- coding:utf-8 -*-
# @Time     :2022/11/11 9:35 下午
# @Author   :CHNJX
# @File     :report_page.py
# @Desc     :报事页面
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

from mini_project.base.app import App

home_repair = (By.LINK_TEXT, "居家维修")
customer_service = (By.LINK_TEXT, "客户服务")
question_input = (By.CSS_SELECTOR, "#content")
commit_button = (MobileBy.XPATH, "//wx-button")
result_text = (By.XPATH,"//wx-text[@class='title']/span[2]")


class ReportPage(App):

    def report_home_repair(self):
        # 小程序要textarea才能进行输入操作
        ele = self.driver.find_element(By.XPATH,"//*[@id='content']/div/textarea")
        ele.send_keys("ceshiyixia")
        self.find_and_click(commit_button)
        self.switch_windows(':VISIBLE')
        return self

    def get_report_result(self) -> str:
        return self.find_element(*result_text).get_element_text()
