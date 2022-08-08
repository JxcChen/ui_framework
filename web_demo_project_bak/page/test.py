# -*- coding:utf-8 -*-
# @Time     :2022/8/5 8:30 下午
# @Author   :CHNJX
# @File     :test.py
# @Desc     :
import importlib.util
import importlib


# def check_module(module_name):
#     ms = importlib.util.find_spec(module_name)
#     if ms is None:
#         print("Module :{} not found".format(module_name))
#         return None
#     else:
#         print("Module:{} can be imported!".format(module_name))
#         return ms
#
#
# def import_module_from_spec(module_spec):
#     m = importlib.util.module_from_spec(module_spec)
#     module_spec.loader.exec_module(m)
#     return m
#
#
# if __name__ == "__main__":
#     ms = check_module("fake_module")
#     ms = check_module("token_helper")
#     if ms:
#         module = import_module_from_spec(ms)
#         print(dir(module))

import importlib.util

def import_source(module_name):
    module_file_path = module_name.__file__
    module_name = module_name.__name__

    module_spec = importlib.util.spec_from_file_location(module_name ,module_file_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir(module))

    msg = "The {module_name} module has the following methods:{methods}"
    print(msg.format(module_name = module_name ,methods = dir(module)))

if __name__ == "__main__":
    import logging
    import_source(logging)

