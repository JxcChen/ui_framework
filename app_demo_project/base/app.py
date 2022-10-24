# -*- coding:utf-8 -*-
# @Time     :2022/7/30 10:09 上午
# @Author   :CHNJX
# @File     :app.py
# @Desc     :app基类
import logging
import subprocess

from app_demo_project.base.base_page import BasePage


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

    def slide_to_element_visible(self, locator):
        """
        滑动到元素可见
        :param locator: 元素定位表达式
        """
        # 获取滑动之前的页面元素
        old_source = self.driver.page_source
        # 获取到窗口大小
        size = self.driver.get_window_size()
        while True:
            try:
                # 获取目标元素
                self.driver.find_element(*locator)
            except Exception as e:
                # 获取不到目标元素 将屏幕往下滑动
                self.swipe_page("down")
                new_source = self.driver.page_source
                if new_source == old_source:
                    self.logger.exception(f"页面中不存在{locator}元素")
                    break
                else:
                    old_source = new_source
            else:
                self.logger.info(f"页面中存在{locator}元素")
            break


def swipe_page(self, direction: str):
    """
    根据方向滑动页面
    :param direction: 需要滑动的方向
    """
    # 获取页面尺寸
    size = self.get_window_size()
    try:
        width_ = size["width"]
        height_ = size["height"]
        if direction == "up":
            # 向上滑动
            self.driver.swipe(start_x=width_ * 0.5, start_y=height_ * 0.2, end_x=width_ * 0.5,
                              end_y=height_ * 0.8, duration=100)
        elif direction == "down":
            self.driver.swipe(start_x=width_ * 0.5, start_y=height_ * 0.8, end_x=width_ * 0.5,
                              end_y=height_ * 0.2)
        elif direction == "left":
            self.driver.swipe(start_x=width_ * 0.8, start_y=height_ * 0.5, end_x=width_ * 0.2,
                              end_y=height_ * 0.5)
        elif direction == "right":
            self.driver.swipe(start_x=width_ * 0.2, start_y=height_ * 0.5, end_x=width_ * 0.8,
                              end_y=height_ * 0.5)

    except Exception as e:
        self.logger.exception(f"向{direction}滑动失败")
    else:
        self.logger.info(f"向{direction}滑动成功")


def get_window_size(self):
    """获取页面大小"""
    try:
        size = self.driver.get_window_size()
    except Exception as e:
        self.logger.exception("获取窗口大小失败")
        raise e
    else:
        self.logger.info("获取窗口大小成功")
        return size
