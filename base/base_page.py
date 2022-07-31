# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:04 上午
# @Author   :CHNJX
# @File     :base_page.py
# @Desc     :page基类
import datetime
import json
import os

import allure
import yaml
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from base.handle_exception import handle_exception


class BasePage:
    _element: WebElement = None
    current_time = 0
    _elements: list[WebElement] = None
    caps = {}

    def __init__(self, driver: WebDriver = None):
        from base.app import App
        from base.web import Web
        if driver is None:
            if self.__class__.__base__ is App:
                self.init_app()
            elif self.__class__.__base__ is Web:
                self.init_web()
            self.driver.implicitly_wait(3)
        else:
            self.driver = driver

    def init_web(self):
        from selenium import webdriver
        # web driver 初始化
        driver_type = os.getenv("browser")
        # 根据用户传入变量打开对应的浏览器
        if driver_type == "firefox":
            self.driver = webdriver.Firefox()
        elif driver_type == 'edge':
            self.driver = webdriver.Edge()
        else:
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def init_app(self):
        from appium import webdriver
        with open(f'{os.path.dirname(__file__)}/capability_conf.yml', encoding='utf-8') as cap:
            cap_conf = yaml.safe_load(cap)
        self.caps = cap_conf['capability']
        self.driver = webdriver.Remote(f"{cap_conf['server']['host']}:{cap_conf['server']['port']}/wd/hub", self.caps)

    # @handle_exception
    def find_element(self, by, locator: str = None) -> WebElement:
        """
        查找元素
        :param by: 可以是元祖或者by对象
        :param locator: 定位符 默认为空  如果不传 by必须传元祖
        :return: 目标元素
        """
        if locator is None:
            self._element = self.driver.find_element(*by)
        else:
            self._element = self.driver.find_element(by, locator)

    def click(self):
        """
        点击元素  需要先查找
        """
        self._element.click()
        return self

    def send(self, key):
        """
        点击元素  需要先查找
        """
        self._element.send_keys(key)
        return self

    def find_and_click(self, by, locator: str = None):
        """
        点击元素
        return 当前页面
        """
        self.find_element(by, locator)
        return self.click()

    def find_and_send(self, key: str, by, locator: str = None):
        """
        点击元素
        return 当前页面
        """
        self.find_element(by, locator)
        return self.send(key)

    def find_elements(self, by, locator: str = None, index: int = None):
        """
        查找全部相关元素
        """
        if index is None:
            if locator is None:
                self._elements = self.driver.find_elements(*by)
            else:
                self._elements = self.driver.find_elements(by, locator)
        if index is not None:
            if locator is None:
                self._element = self.driver.find_elements(*by)[index]
            else:
                self._element = self.driver.find_elements(by, locator)[index]
            return self._element

    def get_elements_text(self):
        if self._elements is not None:
            return [ele.text for ele in self._elements]
        else:
            return

    def get_element_text(self):
        return self._element.text

    def wait_for_click(self, locator, timeout=10):
        """
        等待元素可被点击
        :param locator: 定位符
        :param timeout: 超时时间 默认10秒
        :return: self
        """
        self._element = WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable(locator))
        return self

    def wait_for_visible(self, locator, timeout=10):
        """
        等待元素可被点击
        :param locator: 定位符
        :param timeout: 超时时间 默认10秒
        :return: self
        """
        self._element = WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator))
        return self

    def save_screenshot(self, name: str = None, png_dir: str = None) -> str:
        """
        保存截图
        :param name:截图名称  默认为当前时间
        :param png_dir: 截图存放路径默认存在res/image下
        return 返回完整名称
        """
        if name is None:
            name = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if png_dir is None:
            png_dir = './image'
        png_path = png_dir + '/' + name + '.png'
        self.driver.save_screenshot(png_path)
        # 将截图放到allure中
        with open(png_path, 'rb') as f:
            allure.attach(f.read(), attachment_type=allure.attachment_type.PNG)
        return png_path
