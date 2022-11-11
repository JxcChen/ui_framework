# -*- coding:utf-8 -*-
# @Time     :2022/7/31 3:37 下午
# @Author   :CHNJX
# @File     :test.py
# @Desc     :
import importlib
import re

s = 'This and that.'

# m = re.match('cd',s)
# if m:
#     print(m.group())


s = 'https://www.baidu.com/'
res = re.search(r'^(https|http)://www\.\w+\.(com|edu|net)/$', s)
print(res.group())


s = "<type 'builtin_function_or_method'>"
res = re.search(r'type\s(:?\'\w+\')',s)
print(res.group(1))

s = '10'
res = re.search(r'1[0-2]',s)
print(res.group())


'Thu Jul 22 19:21:19 2004::izsp@dicqdhytvhv.edu::1090549279-4-11'

