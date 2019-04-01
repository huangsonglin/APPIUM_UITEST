#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2018/12/6 13:55'


import os
import requests
import random
import time
import hashlib
from urllib import parse
from Until.YamlRead import *

class V5_ORDER:
    host = 'http://testapp.dcpai.cn/app/'
    headers = {'User-Agent': 'Auction/5.0.0 (iPhone; iOS 11.4.1; Scale/2.00)',
               'Accept-Language': 'zh-Hans-CN;q=1',
               'Connection': 'keep-alive',
               'Content - Type': 'application/x-www-form-urlencoded',
               'clientType': 'IOS'}
    timeout = 3
    Authorization = Config(App_LoginToken).get('Authorization')

    def get_token(self, ):
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

    def logout(self):
        url = self.host + 'interface/mobile/logout_112'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        memberId = Mysql().reslut_replace(f'SELECT id FROM `user` where username={username}')
        data = {"memberId": memberId}
        req = requests.post( url, headers=self.headers, data=data)
        return req

    # 获取卖家信息
    def getSellerCalcInfo_400(self, memberId):
        """
        :param memberId:  获取卖家信息，如果又商品则shopId新增店铺id
        :return:
        """
        url = self.host + 'interface/mobile/pmall/getSellerCalcInfo_400'
        data = {'memberId': memberId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 订单管理--下单初始化
    def buyerPlaceOrderInit_500(self, productId):
        url = self.host + 'interface/mobile/buyerPlaceOrderInit_500'
        data = {'productId': productId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取商品库存
    def getProductInventory_500(self, productId):
        url = self.host + 'interface/mobile/getProductInventory_500'
        data = {'productId': productId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 下单，提交订单
    def buyerPlaceOrder_500(self, productId, quantity, receiverId):
        """
        :param username:
        :param password:
        :param productId: 下单商品ID
        :param quantity:  购买数量
        :param receiverId:  收货地址ID
        :return: orderId（订单ID）
        """
        url = self.host + 'interface/mobile/buyerPlaceOrder_500'
        data = {'productId': productId, 'quantity':quantity, 'receiverId':receiverId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    #  买家订单全部列表
    def findAllBuyerOrderPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findAllBuyerOrderPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 待付款列表
    def findBuyerWaitPayPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findBuyerWaitPayPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 待发货列表
    def findBuyerWaitSendPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findBuyerWaitSendPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 待收货列表
    def findBuyerWaitReceivePage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findBuyerWaitReceivePage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req


    # 待评价列表
    def findBuyerWaitCommentPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findBuyerWaitCommentPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 买家订单详情
    def findBuyerOrderDetail_500(self, orderId):
        url = self.host + 'interface/mobile/findBuyerOrderDetail_500'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 支付初始化
    def payBuyerOrderInit_500(self, orderId):
        url = self.host + 'interface/mobile/payBuyerOrderInit_500'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 卖家订单全部列表
    def findAllSellerOrderPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findAllSellerOrderPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 订单待付款列表
    def findSellerWaitPayPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findSellerWaitPayPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 订单待发货列表
    def findSellerWaitSendPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findSellerWaitSendPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 已发货列表
    def findSellerWaitReceivePage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findSellerWaitReceivePage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 订单待评价列表
    def findSellerWaitCommentPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findSellerWaitCommentPage_500'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 卖家订单详情
    def findSellerOrderDetail_500(self, orderId):
        url = self.host + 'interface/mobile/findSellerOrderDetail_500'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 发货初始化
    def sellerOrderSendInit_500(self, orderId):
        url = self.host + 'interface/mobile/sellerOrderSendInit_500'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 修改价格初始化
    def changeOrderPriceInit_500(self, orderId):
        url = self.host + 'interface/mobile/changeOrderPriceInit_500'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 修改价格
    def changeOrderPrice_500(self, orderId, hammerPrice, postage):
        """
        :param orderId: 订单ID
        :param hammerPrice:修改后的价格
        :return:
        """
        url = self.host + 'interface/mobile/changeOrderPrice_500'
        data = {'orderId': orderId, 'hammerPrice':hammerPrice, "postage":postage}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 新增申请退款/退货初始化
    def buyerOrderReturnAddInit_420(self, orderItemId):
        url = self.host + 'interface/mobile/buyerOrderReturnAddInit_420'
        data = {'orderItemId': orderItemId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 申请退货
    def buyerOrderReturnApply_420(self,orderItemId, reasonDesc ,reasonImages=None,reasonType="O_T"):
        """
        执行成功的前提条件： orderItemId 的状态必须是S--卖家以发货的状态
        :param username:
        :param password:
        :param orderItemId:   订单Item号
        :param reasonImages:    图片
        :param reasonType:      原因 N_S：卖家不发货  O_T：其他原因
        :param reasonDesc:      	其他原因
        :return:
        """
        url = self.host + 'interface/mobile/buyerOrderReturnApply_420'
        data = {'orderItemId': orderItemId,'reasonImages':reasonImages,
                'reasonType':reasonType,'reasonDesc':reasonDesc}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url=url, data=data, headers=self.headers)
        return req

    # 修改申请退款/退货初始化
    def buyerOrderReturnEditInit_420(self,orderReturnId):
        url = self.host + 'interface/mobile/buyerOrderReturnEditInit_420'
        data = {'orderReturnId':orderReturnId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 退款|退货同意
    def sellerOrderReturnAgree_420(self, orderReturnId, payword):
        url = self.host + 'interface/mobile/sellerOrderReturnAgree_420'
        data = {'id': orderReturnId, 'payPassword':MD5_encryption().md5(payword)}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 买家售后列表
    def findBuyerOrderReturnPage_420(self,page=1,rows=20):
        url = self.host + 'interface/mobile/findBuyerOrderReturnPage_420'
        data = {'page': page,'rows':rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 家售后详情
    def findBuyerOrderReturnDetail_420(self,orderReturnId):
        url = self.host + 'interface/mobile/findBuyerOrderReturnDetail_420'
        data = {'orderReturnId': orderReturnId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 退货发货初始化
    def buyerOrderReturnSendInit_420(self,orderReturnId):
        url = self.host + 'interface/mobile/buyerOrderReturnSendInit_420'
        data = {'orderReturnId': orderReturnId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 卖家售后列表
    def findSellerOrderReturnPage_420(self,page=1,rows=20):
        url = self.host + 'interface/mobile/findSellerOrderReturnPage_420'
        data = {'page': page, 'rows': rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 卖家售后详情
    def findSellerOrderReturnDetail_420(self, orderReturnId ):
        url = self.host + 'interface/mobile/findSellerOrderReturnDetail_420'
        data = {'orderReturnId': orderReturnId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 卖家同意/不同意售后初始化
    def sellerOrderReturnAgreeInit_420(self, orderReturnId):
        url = self.host + 'interface/mobile/sellerOrderReturnAgreeInit_420'
        data = {'orderReturnId': orderReturnId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 账户
    def getAccountInfo_230(self):
        url = self.host + 'interface/mobile/getAccountInfo_230'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 发货
    def sellerOrderSend_420(self, orderId, express, trackingNum):
        url = self.host + 'interface/mobile/sellerOrderSend_420'
        data = {'orderId':orderId, 'express':express, 'trackingNum':trackingNum}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 买家催货
    def EXPEDITING(self, orderId):
        url = self.host + 'interface/mobile/memberChangeOrderStatus_112'
        data = {'orderId': orderId, 'type': "N"}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 取消订单
    def CancelOrder(self, orderId):
        url = self.host + 'interface/mobile/memberChangeOrderStatus_112'
        data = {'orderId': orderId, 'type': "C"}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 确认收货
    def RECEIVING(self, orderId, payword):
        url = self.host + 'interface/mobile/memberChangeOrderStatus_112'
        data = {'orderId': orderId, 'type': "R", "payPwd":MD5_encryption().md5(payword)}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 卖家关闭订单
    def sellerCancelOrder_420(self, orderId):
        url = self.host + 'interface/mobile/sellerCancelOrder_420'
        data = {'orderId': orderId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 获取地址
    def doGetAddress_112(self):
        url = self.host + 'interface/mobile/doGetAddress_112'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 获取卖家统计信息
    def getSellerCalcInfo_400(self, MemberId):
        url = self.host + 'interface/mobile/pmall/getSellerCalcInfo_400'
        data = {'memberId': MemberId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 订单评价数量
    def countOrderComment_112(self, MemberId):
        url = self.host + 'interface/mobile/pmall/countOrderComment_112'
        data = {'memberId': MemberId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

if __name__ == '__main__':
    req = V5_ORDER().getAccountInfo_230()
    print(req.text)