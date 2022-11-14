# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:04 上午
# @Author   :CHNJX
# @File     :base_page.py
# @Desc     :page基类
import datetime
import logging
import os
from time import sleep

import allure
import yaml
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from web_sa_4s_workorder.base.handle_exception import handle_exception
from web_sa_4s_workorder.project_logger import ProjectLogger


class BasePage:
    _element: WebElement = None
    _elements: list[WebElement] = None
    current_time = 0
    caps = {}

    def __init__(self, driver: WebDriver = None):
        self.logger = ProjectLogger().get_logger()
        from web_sa_4s_workorder.base.app import App
        from web_sa_4s_workorder.base.web import Web
        if driver is None:
            if self.__class__.__base__ is App:
                self.init_app()
            elif self.__class__.__base__ is Web:
                self.init_web()
            self.driver.implicitly_wait(5)
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

    @handle_exception
    def find_element(self, by, locator: str = None) -> WebElement:
        """
        查找元素
        :param by: 可以是元祖或者by对象
        :param locator: 定位符 默认为空  如果不传 by必须传元祖
        :return: 目标元素
        """
        self.logger.info(f'查找元素 by：{by},locator:{locator}')
        try:
            if locator is None:
                self._element = self.driver.find_element(*by)
            else:
                self._element = self.driver.find_element(by, locator)
        except Exception as e:
            self.logger.error(f'查找元素 by：{by} 失败,locator:{locator}')
            self.logger.error(e.__str__())
            self.logger.info('开始判断是否有存在黑名单元素')
            raise e
        return self._element

    def click(self):
        """
        点击元素  需要先查找
        """
        self.logger.info('点击元素')
        try:
            self._element.click()
        except Exception as e:
            self.logger.error('点击元素失败')
            self.logger.error(e.__str__())
            raise e
        return self

    def send(self, key):
        """
        点击元素  需要先查找
        """
        self.logger.info(f'输入 key： {key}')
        self._element.send_keys(key)
        return self

    def find_and_click(self, by, locator: str = None):
        """
        点击元素
        return 当前页面
        """
        self.logger.info(f'查找并点击元素 by：{by} locator:{locator}')
        self.find_element(by, locator)
        return self.click()

    def find_and_send(self, key: str, by, locator: str = None):
        """
        点击元素
        return 当前页面
        """
        self.logger.info(f'查找并输入内容 by：{by} locator:{locator} key:{key}')
        self.find_element(by, locator)
        return self.send(key)

    def find_elements(self, by, locator: str = None, index: int = None):
        """
        查找全部相关元素
        """
        self.logger.info(f'查找全部相关元素 by：{by} locator:{locator} 第{index}个')
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

    def get_elements_text(self) -> list:
        """
        获取元素的文本属性列表
        """
        self.logger.info(f'获取元素的文本属性列表')
        if self._elements is not None:
            return [ele.text for ele in self._elements]
        else:
            return []

    def get_element_text(self) -> str:
        """
        获取元素的文本属性
        """
        self.logger.info(f'获取元素的文本属性')
        return self._element.text

    def wait_for_click(self, locator, timeout=15):
        """
        等待元素可被点击
        :param locator: 定位符
        :param timeout: 超时时间 默认10秒
        :return: self
        """
        self.logger.info(f'等待元素可被点击 locator：{locator} timeout：{timeout}')
        self._element = WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable(locator))
        return self

    def wait_for_visible(self, locator, timeout=10):
        """
        等待元素可见
        :param locator: 定位符
        :param timeout: 超时时间 默认10秒
        :return: self
        """
        self.logger.info(f'等待元素可见 locator：{locator} timeout：{timeout}')
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
        self.logger.info(f'进行截图 name：{name} png_dir：{png_dir}')
        self.driver.save_screenshot(png_path)
        # 将截图放到allure中
        with open(png_path, 'rb') as f:
            allure.attach(f.read(), attachment_type=allure.attachment_type.PNG)
        return png_path

    # ******************* web *************************
    def scroll_to_bottom(self):
        """
        滑动到页面底部
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def switch_windows(self, pattern: str):
        """
        切换页面
        :param pattern: 对应页面中title存在元素
        """
        sleep(1)
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            if pattern in self.driver.title:
                break
