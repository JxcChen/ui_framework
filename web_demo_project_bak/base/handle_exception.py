# -*- coding:utf-8 -*-
# @Time     :2022/7/30 12:51 下午
# @Author   :CHNJX
# @File     :handle_exception.py
# @Desc     :处理异常弹框

from selenium.webdriver.common.by import By

from web_sa_4s_workorder.project_logger import ProjectLogger

_black_list = [(By.XPATH, "//*[@resource-id='iv_close']"),
               (By.XPATH, "//*[text='下一步']"),
               (By.XPATH, "//*[text='等待']"),
               (By.XPATH, "//*[text='取消']"),
               (By.XPATH, "//*[text='等待']"),
               (By.XPATH, "//*[text='我知道了']"), ]
_max_time = 3
logger = ProjectLogger().get_logger()


def handle_exception(func):
    """
    处理错误弹框问题
    :param func: 需要被修饰的方法
    """
    def close_exception(*args, **kwargs):
        from app_demo_project.base.base_page import BasePage
        # 获取实例  args[0] = self
        instance: BasePage = args[0]
        try:
            res = func(*args, **kwargs)
            instance.current_time = 0
            return res
        except Exception as e:
            if _max_time <= instance.current_time:
                logger.error(f'元素查找失败 不存在黑名单内元素')
                raise e
            instance.current_time += 1
            logger.error(f'元素查找失败 by：{args[1]},locator：{args[2]} 进行错误处理 当前处理次数：{instance.current_time}')
            # 查看是否存在黑名单内容  有则进行关闭
            for black in _black_list:
                ele = instance.find_elements(black)
                if ele:
                    ele[0].click()
                    # 进行递归
                    return close_exception(*args, **kwargs)
            # 截图
            instance.save_screenshot()
            raise e

    return close_exception
