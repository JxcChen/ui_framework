# -*- coding:utf-8 -*-
# @Time     :2022/8/4 8:29 下午
# @Author   :CHNJX
# @File     :token_helper.py
# @Desc     :获取token
import requests


def get_token():
    captchaKey = requests.get("https://sa-test.pmaicloud.com/sa-auth/captcha").json()["data"]['captchaKey']
    token_param = {"username": "chenjx",
                   "password": "123456",
                   "grant_type": "password",
                   "captchaKey": captchaKey,
                   "scope": "cloud",
                   "captchaCode": "8888"}
    return requests.post(url="https://sa-test.pmaicloud.com/sa-auth/oauth/token",
                         data=token_param,
                         headers={"Authorization": "Basic c2EtY2xvdWQ6c2EtY2xvdWQ="}).text
