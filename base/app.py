# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:09 上午
# @Author   :CHNJX
# @File     :app.py
# @Desc     :app基类
import logging
import subprocess

from appium import webdriver

from base.base_page import BasePage


def back_handle(func):
    def handle(*args, **kwargs):
        instance: App = args[0]
        try:
            func(*args, **kwargs)
        except Exception as e:
            current_focus = subprocess.check_output('adb shell dumpsys activity activities | grep mFocusedActivity',
                                                    shell=True).decode('utf-8')
            if instance.caps['appPackage'] not in current_focus:
                logging.error('没有找到主页元素')
                instance.save_screenshot('返回主页错误')
                instance.start()
                raise e
            instance.driver.back()
            return handle(*args, **kwargs)

    return handle


class App(BasePage):

    def start(self):
        self.driver.launch_app()
        return self

    def restart(self):
        # 重启 app
        self.driver.close_app()
        self.driver.launch_app()

    def stop(self):
        # 停止 app
        self.driver.quit()

    @back_handle
    def back_to_main(self, by, locator: str = None):
        """
        反回到首页
        :param by: 定位方式
        :param locator: 首页独有的元素定位符
        """
        if locator is None:
            self.find_element(*by)
        else:
            self.find_element(by, locator)
