# -*- coding:utf-8 -*-
# @Time     :2022/8/9 14:21
# @Author   :CHNJX
# @File     :test.py
# @Desc     :
import sys
from functools import reduce
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_web():

    options = Options()
    options.debugger_address = 'https://www.vmall.com/product/10086238622707.html#2601010388206'
    driver = webdriver.Chrome(options=options)


if __name__ == '__main__':
    init_web()
