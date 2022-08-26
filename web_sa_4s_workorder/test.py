# -*- coding:utf-8 -*-
# @Time     :2022/8/9 14:21
# @Author   :CHNJX
# @File     :test.py
# @Desc     :
import sys
from functools import reduce


def reduce_test():
    # 累加功能： 1~5做累加  [1,2,3,4,5]  = > (((1+2) + 3) + 4)
    def f(x, y):
        result = x - y
        return result

    print(sum([1, 2, 3, 4, 5]))
    print(reduce(f, [1, 2, 3, 4, 5]))


reduce_test()