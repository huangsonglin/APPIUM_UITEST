#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/26 14:08'


import os
import requests
import random
import time
import hashlib
from urllib import parse
import urllib.response
import urllib.request
from Until.YamlRead import *


class Four_Vesion_Api:
    host = Config(CONFIG_FILE).get("host")
    headers =  Config(CONFIG_FILE).get("headers")
    timeout = 3
    # Authorization = Config(App_LoginToken).get('Authorization')

    def findMyHoldProductPage_420(self, rows=20, page=1):
        url = self.host + 'interface/mobile/findMyHoldProductPage_420'
        data = {'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findMyInAucProductPage_420(self, rows=20, page=1):
        url = self.host + 'interface/mobile/findMyInAucProductPage_420'
        data = {'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findMySoldOutProductPage_420(self, rows=20, page=1):
        url = self.host + 'interface/mobile/findMyInAucProductPage_420'
        data = {'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 更新秒啪商品初始化
    def updateMyAppProductInit_270(self, lotId):
        url = self.host + 'interface/mobile/updateMyAppProductInit_270'
        data = {'lotId': lotId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 发帖-帖子分类
    def findAllPostType_320(self):
        url = self.host + 'interface/mobile/pmall/findAllPostType_320'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 龖江湖*查看公告
    def findOfficialBulletin_300(self):
        url = self.host + 'interface/mobile/pmall/findOfficialBulletin_300'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 龖江湖* 查看置顶
    def findOfficialTopPost_300(self):
        url = self.host + 'interface/mobile/pmall/findOfficialTopPost_300'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 查看热门帖子
    def findHotPostPage_300(self, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/findHotPostPage_300'
        data = {'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 关注
    def findFocusByFasId_204(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findFocusByFasId_204'
        data = {'page': page, 'rows': rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 帖子详情评论列表
    def findTopReplyByPostId_300(self, postId, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/findTopReplyByPostId_300'
        data = {'postId': postId, 'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def sendAuthenticationCode_112(self, phone):
        data = {"phoneNum": phone}
        url = self.host + 'interface/mobile/pmall/sendAuthenticationCode_112'
        req = requests.post(url, data=data, headers=self.headers)

    def searchPostPage_300(self, keyword, page=1, rows=10, sort='H'):
        url = self.host + 'interface/mobile/pmall/searchPostPage_300'
        data = {'keyword': keyword, 'page': page, 'rows': rows, 'sort': sort}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

if __name__ == '__main__':
    req = Down_V5Api().findFocusByFasId_204()
    print(req.text)