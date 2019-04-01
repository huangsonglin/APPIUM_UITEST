#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2018/12/17 17:11'

import os
import requests
import random
import time
import hashlib
from urllib import parse
from Until.YamlRead import *

class LZShop:
    host = 'http://testapp.dcpai.cn/app/'
    headers = {'User-Agent': 'Auction/5.0.0 (iPhone; ANDROID 11.4.1; Scale/2.00)',
               'Accept-Language': 'zh-Hans-CN;q=1',
               'Connection': 'keep-alive',
               'Content - Type': 'application/x-www-form-urlencoded',
               'clientType': 'ANDROID'}
    timeout = 3
    Authorization = Config(App_LoginToken).get('Authorization')

    def get_token(self):
        url = 'interface/mobile/pmall/loginByPhone_220'
        hl = hashlib.md5()
        hl.update(str(password).encode(encoding='utf-8'))
        pw = (hl.hexdigest())
        data = {"phoneNum": username, "pwd": pw}
        lgurl = self.host + url
        req = requests.post(lgurl, data=data, headers=self.headers)
        if req.status_code == 200:
            Authorization = 'Bearer ' + req.json()['accessToken']
            return Authorization
        else:
            return None

    # 龙珠商城首页(商品列表）
    def findCreditProductPage_500(self, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/findCreditProductPage_500'
        data = {'page':page, 'rows':rows}
        req = requests.post(url=url, data=data, headers= self.headers,timeout= self.timeout)
        return req

    # 龙珠商品详情
    def getCreditProductDetail_500(self, creditProductId):
        url = self.host + 'interface/mobile/pmall/getCreditProductDetail_500'
        data = {'creditProductId': creditProductId}
        req = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 龙珠商品兑换记录
    def findCreditExchangeRecord_500(self,  page=1, rows=10):
        url = self.host + 'interface/mobile/findCreditExchangeRecord_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取消费记录
    def findCreditRecord_500(self,  page=1, rows=100):
        url = self.host + 'interface/mobile/findCreditRecord_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看物流信息
    def findCreditProductOrderExpress_500(self, orderNum):
        """
        :param username:
        :param password:
        :param orderNum: 龙珠商品订单号
        :return:
        """
        url = self.host + 'interface/mobile/findCreditProductOrderExpress_500'
        data = {'orderNum': orderNum}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 兑换龙珠商品
    def buyCreditProduct_500(self,  creditProductId, deliverAddressId, num):
        """
        :param username:
        :param password:
        :param creditProductId: 龙珠商品ID
        :param deliverAddressId:    选择的地址信息ID
        :param num: 购买数量
        :return:
        """
        url = self.host + 'interface/mobile/buyCreditProduct_500'
        data = {'creditProductId': creditProductId, "deliverAddressId":deliverAddressId, "num":num}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取用户信息
    def getMemberDetailInfo_112(self):
        url = self.host + 'interface/mobile/getMemberDetailInfo_112'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url,  headers=self.headers, timeout=self.timeout)
        return req

    # 获取用户龙珠数量
    def findMemberCredit_220(self):
        url = self.host + 'interface/mobile/findMemberCredit_220'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, headers=self.headers, timeout=self.timeout)
        return req

if __name__ == '__main__':
    req = LZShop().findMemberCredit_220()
    # req = LZShop().getMemberDetailInfo_112()
    print(req.text)