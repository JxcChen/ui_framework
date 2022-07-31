# -*- coding:utf-8 -*-
# @Time     :2022/7/31 6:04 下午
# @Author   :CHNJX
# @File     :utils.py
# @Desc     :方法模块
import logging


def replace_form_2_actual(form_param: str, actual_dict: dict):
    form_param = form_param.replace('$', '')
    if actual_dict.get(form_param):
        return actual_dict[form_param]
    else:
        logging.error('没有传参数')
        return form_param
