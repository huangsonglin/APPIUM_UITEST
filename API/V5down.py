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
    timeout = 1
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

    # 话题搜索
    def searchPostPage_300(self, keyword, typeId="", page=1, rows=20, sort='H'):
        url = self.host + 'interface/mobile/pmall/searchPostPage_300'
        data = {'keyword': keyword, "typeId":typeId, 'page': page, 'rows': rows, 'sort': sort}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 藏品搜索
    def searchLotPage_420(self, keyword, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/searchLotPage_420'
        data = {'keyword': keyword, 'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 搜索藏友
    def findESMemberPage_204(self, keyword, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/findESMemberPage_204'
        data = {'keyword': keyword, 'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 搜索门派
    def searchForumPage_300(self, keyword, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/searchForumPage_300'
        data = {'keyword': keyword, 'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 广告
    def findAdvertiseContent_260(self, position, deviceType="ANY_TYPE"):
        """
        :param deviceType: ANY_TYPE（选填，设备纵横比）
        :param position:    P1:拍场广告(已经无效)
                            P2：精品广告（android暂时使用 P1代替）
                            P3：开机广告
                            P4：首页顶部广告
                            P5：首页中下部运营广告
                            P6：精选页广告
                            P9：门派广告
                            P10：积分商城首页广告图
                            P11：龘商城商品页广告图
                            P12：龘商城店家页广告图
                            P13：龘江湖精选页广告图
                            P14：龘江湖视频页广告图
                            P15：龘藏直播页广告图
        :return:
        """
        url = self.host + 'interface/mobile/pmall/findAdvertiseContent_260'
        data = {"deviceType": deviceType, "position": position}
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req



if __name__ == '__main__':
    req = Four_Vesion_Api().findAdvertiseContent_260("P4")
    print(req.text)