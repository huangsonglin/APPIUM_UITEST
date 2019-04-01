#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2018/11/19 9:21'

'''
龖藏店铺--11.19版本
'''

import os
import requests
import random
import time
import hashlib
from urllib import parse
import urllib.response
import urllib.request
from Until.YamlRead import *


class v5:
    host = 'http://testapp.dcpai.cn/app/'
    headers= {'User-Agent':'Auction/5.0.0 (iPhone; ANDROID 11.4.1; Scale/2.00)',
          'Accept-Language':'zh-Hans-CN;q=1',
          'Connection':'keep-alive',
          'Content - Type':'application/x-www-form-urlencoded',
          'clientType':'ANDROID'}
    timeout = 3
    Authorization = Config(App_LoginToken).get('Authorization')


    def get_token(self,username,password):
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

    # 获取用户的权限
    def getMemberPrivileges_500(self):
        """
        :param username: 想查看的用户账号
        :param password:    用户密码
        :return:
        """
        self.headers.update(Authorization=self.Authorization)
        url = self.host + 'interface/mobile/getMemberPrivileges_500'
        req = requests.post(url,headers=self.headers,timeout=self.timeout)
        return req

    # 获取所有已激活店铺
    def findActivationShopPage_500(self,page=1,rows=10):
        url = self.host + 'interface/mobile/pmall/findActivationShopPage_500'
        data = {'page':page,'rows':rows}
        req = requests.post(url, data= data, headers=self.headers, timeout=self.timeout)
        return req

    # 店铺分享
    def findShopShareInfo_500(self, shopId):
        url = self.host + 'interface/mobile/pmall/findShopShareInfo_500'
        data ={'shopId':shopId}
        req = requests.post(url, data=data, headers= self.headers, timeout= self.timeout)
        return req

    # 获取店铺详情页
    def findShopDetail_500(self, shopId):
        url = self.host + 'interface/mobile/pmall/findShopDetail_500'
        data = {'shopId':shopId}
        req = requests.post(url, data=data, headers= self.headers, timeout= self.timeout)
        return req

    # 修改店铺初始化
    def updateMyShopInit_500(self, shopId):
        url = self.host + 'interface/mobile/updateMyShopInit_500'
        data = {'shopId': shopId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 修改店铺
    def updateMyShop_500(self, shopId, shopname, icon, backgroundMap, shopAdvertiseList=None,shopRecommendIdList=None):
        """
        :param username:
        :param password:
        :param shopId:  店铺ID
        :param shopname:    店铺名字
        :param icon:        店铺头像
        :param backgroundMap:   店铺背景图
        :param shopAdvertiseList:   店铺广告列表，要求有序且不超过10
        :param shopRecommendIdList: 推荐商品列表，只允许：取消推荐，即（推荐商品ID列表只少不多）
        :return:
        """
        url = self.host + 'interface/mobile/updateMyShop_500'
        data = {'id': shopId, 'name':shopname,'icon':icon, 'backgroundMap':backgroundMap,
                'shopAdvertiseList':shopAdvertiseList, 'shopRecommendIdList':shopRecommendIdList}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
        return req

    # 店铺所有商品列表
    def findAllMyShopProductPage_500(self, page=1, rows=10):
        '''
        :param username: 账户名称
        :param password: 账户密码
        :param shopId:   商铺ID
        :param page:     分页参数-页
        :param rows:     分页参数-行
        :return:
        '''
        url = self.host + 'interface/mobile/findAllMyShopProductPage_500'
        data ={'page':page, 'rows':rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取我的门派
    def findMyForum_500(self):
        url = self.host + 'interface/mobile/findMyForum_500'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 获取我的拍场
    def findAllMyAuctionList_500(self, bidModel):
        """
        :param username:
        :param password:
        :param bidModel:  竞价类型 bidModel（竞价模式，AUC_DELAY秒啪、AUC_BID轰啪）
        :return:
        """
        url = self.host + 'interface/mobile/findAllMyAuctionList_500'
        data = {'bidModel':bidModel}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 我发布的帖子列表
    def findMyPublishPostPage_500(self, page=1, rows=10):
        url = self.host + 'interface/mobile/findMyPublishPostPage_500'
        data = {'page':page, 'rows':rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 我参与的帖子列表
    def findMyJoinPostPage_500(self, page=1, rows=10):
        url = self.host + 'interface/mobile/findMyJoinPostPage_500'
        data = {'page':page, 'rows':rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取店铺商品分类列表
    def findAllShopPrdCategoryList_500(self, shopId):
        url = self.host + 'interface/mobile/pmall/findAllShopPrdCategoryList_500'
        data = {'shopId':shopId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    #  获取我的店铺商品分类列表
    def findMyShopPrdCategoryList_500(self):
        url = self.host + 'interface/mobile/findMyShopPrdCategoryList_500'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req


    # 新增分类
    def addShopPrdCategory_500(self, name):
        """
        :param username:
        :param password:
        :param name:    类别名称
        :return:
        """
        url = self.host + 'interface/mobile/addShopPrdCategory_500'
        data = {'name': name}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 编辑店铺商品分类顺序
    def updateShopPrdCategoryOrder_500(self, categoryIdList):
        """
        :param username:
        :param passwrod:
        :param categoryIdList: 类别ID列表
        :return:
        """
        url = self.host + 'interface/mobile/updateShopPrdCategoryOrder_500'
        data = {'categoryIdList': categoryIdList}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 编辑店铺商品分类
    def updateShopPrdCategory_500(self, categoryId, name):
        """
        :param username:
        :param passwrod:
        :param categoryId:  类别ID
        :param name:        类名
        :return:
        """
        url = self.host + 'interface/mobile/updateShopPrdCategory_500'
        data = {'categoryId': categoryId, 'name':name}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 删除该店铺商品分类
    def deleteShopPrdCategory_500(self, categoryId):
        url = self.host + 'interface/mobile/deleteShopPrdCategory_500'
        data = {'categoryId': categoryId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取店铺所有分类(官方分类)
    def findAllShopCategoryList_500(self):
        url = self.host + 'interface/mobile/pmall/findAllShopCategoryList_500'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 未上架商品
    def findMyHoldProductPage_500(self, bidModel=None, rows=20, page=1):
        '''
        :param username:
        :param password:
        :param bidModel:    bidModel,非必填，不填表示全部，值为PRODUCT_SHOP，查询商城商品，值为AUC_BID 查询轰拍商品，值为AUC_DELAY查询秒拍商品
        :return:
        '''
        url = self.host + 'interface/mobile/findMyHoldProductPage_500'
        data = {'bidModel': bidModel, 'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 已上架商品
    def findMyInAucProductPage_500(self, bidModel=None, rows=10,page=1):
        '''
        :param username:
        :param password:
        :param bidModel:    bidModel,非必填，不填表示全部，值为PRODUCT_SHOP，查询商城商品，值为AUC_BID 查询轰拍商品，值为AUC_DELAY查询秒拍商品
        :return:
        '''
        url = self.host + 'interface/mobile/findMyInAucProductPage_500'
        data = {'bidModel': bidModel, 'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 已成交商品
    def findMySoldOutProductPage_500(self, bidModel=None, rows=10, page=1):
        '''
        :param username:
        :param password:
        :param bidModel:    bidModel,非必填，不填表示全部，值为PRODUCT_SHOP，查询商城商品，值为AUC_BID 查询轰拍商品，值为AUC_DELAY查询秒拍商品
        :return:
        '''
        url = self.host + 'interface/mobile/findMySoldOutProductPage_500'
        data = {'bidModel': bidModel, 'rows': rows, 'page': page}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 添加店铺商品
    def addAppShopProduct_500(self, images, video, videoImage, name,desc, waitPrice, originalPrice,salesPrice,
                              shopCategory,dcCategory,inAuction,single,inventory,freePost,postage):
        """
        :param username:
        :param password:
        :param images:  图片
        :param video:   视频
        :param videoImage: 视频封面图片
        :param name:    商品名称
        :param desc:    商品描述
        :param waitPrice:   是否展示/估价待询    True/False
        :param originalPrice:   商品原价
        :param salesPrice:      优惠价
        :param shopCategory:    自定义分类
        :param dcCategory:      藏品类型
        :param inAuction:       是否上架 True/False
        :param single:          是否单品 True/False
        :param inventory:       库存
        :param freePost:        是否包邮 True/False
        :param postage:         邮费
        :return:
        """
        url = self.host + 'interface/mobile/addAppShopProduct_500?'
        data = {'name':name, "images":images, 'desc':desc, 'video':video, 'videoImage':videoImage, 'waitPrice':waitPrice
                ,'originalPrice':originalPrice, 'salesPrice':salesPrice, 'shopCategory':shopCategory, 'dcCategory':dcCategory,
                'inAuction':inAuction, 'single':single, 'inventory':inventory, 'freePost':freePost, 'postage':postage}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查询店铺商品详情页（不包含其他商品，供店家查询编辑）店家调用
    def myShopProductDetail_500(self, productId):
        url = self.host + 'interface/mobile/myShopProductDetail_500'
        data = {'productId':productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查询店铺商品详情页（包含其他商品） 买家调用
    def  myShopProductDetailWithOther_500(self, productId, buyer=None, privatePriceId=None):
        """
        :param productId:  商品ID
        :param buyer:      如果是副本，必填buyer,买家id, 不填就是普通详情页
        :param privatePriceId:      如果是副本，privatePriceId 副本id, 不填就是普通详情页
        :return:
        """
        url = self.host + 'interface/mobile/pmall/myShopProductDetailWithOther_500'
        data ={'productId':productId, 'buyer':buyer, 'privatePriceId':privatePriceId}
        req = requests.post(url, data=data, headers= self.headers, timeout= self.timeout)
        return req

    # 下架店铺商品
    def offShelfShopProduct_500(self, productId):
        url = self.host + 'interface/mobile/offShelfShopProduct_500'
        data = {'productId':productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查询分类下的商品
    def myShopProductOfCategoryPage_500(self, shopId, categoryId, sort, order, page=1, rows=100):
        """
        :param shopId:  店铺ID 必填
        :param categoryId:  商家自定义分类id
        :param sort:    sort 综合，salesTime新品，observerCount热度，salesPrice价钱
        :param order:   DESC,ASC
        :param page:
        :param rows:
        :return:
        """
        url = self.host + 'interface/mobile/pmall/myShopProductOfCategoryPage_500'
        data = {'shopId':shopId , 'categoryId':categoryId, 'sort':sort, 'order':order, 'page':page, 'rows':rows}
        req = requests.post(url ,data=data, headers= self.headers, timeout= self.timeout)
        return req

    # 编辑商品
    def updateShopProduct_500(self, id, images, video, videoImage, name, desc, waitPrice, originalPrice,salesPrice,
                              shopCategory,dcCategory,inAuction,single,inventory,freePost,postage):
        url = self.host + 'interface/mobile/updateShopProduct_500'
        data = {'id':id, 'name': name, "images": images, 'desc': desc, 'video': video, 'videoImage': videoImage,
                'waitPrice': waitPrice, 'originalPrice': originalPrice, 'salesPrice': salesPrice,
                'shopCategory': shopCategory,'dcCategory': dcCategory,'inAuction': inAuction,
                'single': single, 'inventory': inventory, 'freePost': freePost,'postage': postage}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 我的店铺--我的商品，商家用
    def myShopProductPage_500(self, page=1, rows= 1000):
        url =  self.host + 'interface/mobile/myShopProductPage_500'
        data = {'page':page, 'rows':rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def myShopAllProductCount_500(self, memberId):
        url = self.host + 'interface/mobile/pmall/myShopAllProductCount_500'
        data = {"memberId": memberId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req


    # 店铺信息--商品，买家用
    def myShopAllProductPage_500(self, memberId, page=1, rows= 20):
        """
        :param memberId: 店主ID
        :param page:
        :param rows:
        :return:
        """
        url = self.host + 'interface/mobile/pmall/myShopAllProductPage_500'
        data = {'memberId':memberId, 'page':page, 'rows':rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    #  商城精品
    def myShopHomeProductPage_500(self, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/myShopHomeProductPage_500'
        data = {'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 推荐
    def recommend_500(self, productId):
        url = self.host + 'interface/mobile/recommend_500'
        data = {'productId':productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 取消推荐
    def unRecommend_500(self, productId):
        url = self.host + 'interface/mobile/unRecommend_500'
        data = {'productId':productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 设置副本
    def privatePrice_500(self, productId, price):
        """
        :param username:
        :param password:
        :param productId:   商品ID
        :param price:       副本价格
        :return:
        """
        url = self.host + 'interface/mobile/privatePrice_500'
        data = {'productId':productId, 'price':price}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 取消副本
    def deletePrivatePrice_500(self, productId):
        url = self.host + 'interface/mobile/deletePrivatePrice_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查询副本列表
    def findMyPrivateProductPage_500(self):
        url = self.host + 'interface/mobile/findMyPrivateProductPage_500'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 查询分享信息
    def findProductShareInfo_500(self, productId):
        url = self.host + 'interface/mobile/pmall/findProductShareInfo_500'
        data = {'productId': productId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 点赞
    def addProductUpvote_500(self, productId):
        url = self.host + 'interface/mobile/addProductUpvote_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 取消点赞
    def deleteProductUpvote_500(self, productId):
        url = self.host + 'interface/mobile/deleteProductUpvote_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 设置恭请
    def reShow_500(self, productId):
        url = self.host + 'interface/mobile/reShow_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 取消恭请
    def unReShow_500(self, productId):
        url = self.host + 'interface/mobile/unReShow_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req


    # 参与的藏品
    def findJoinLotByMemberId_420(self, memberId, page=1, rows=100):
        url = self.host + 'interface/mobile/pmall/findJoinLotByMemberId_420'
        data = {'memberId':memberId, 'page':page, 'rows':rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 用户收藏商品
    def addShopProductFavorite_500(self, productId):
        url = self.host + 'interface/mobile/addShopProductFavorite_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 用户取消收藏商品
    def deleteProductFavorite_500(self, productId ):
        url = self.host + 'interface/mobile/deleteProductFavorite_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 删除商品
    def deleteAppShopProduct_500(self, productId):
        url = self.host + 'interface/mobile/deleteAppShopProduct_500'
        data = {'productId': productId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 新增收货地址
    def saveOrUpdateDeliverAddr_112(self, detailAddr, postalcode, receiverName, receiverPhone, strucAddr):
        url = self.host + 'interface/mobile/saveOrUpdateDeliverAddr_112'
        memberID = Mysql().reslut_replace(f'SELECT id FROM `user` WHERE username={username}')
        data = {'detailAddr': detailAddr, 'memberId': memberID, 'postalcode': postalcode,
                'receiverName': receiverName,
                'receiverPhone': receiverPhone, 'strucAddr': strucAddr}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 支付申请
    def payApply_420(self, amount, applyItemId, payFor, payType):
        url = self.host + 'interface/mobile/payApply_420'
        data = {'amount': amount,  # 金额
                'applyItemId': applyItemId,  # 申请对象ID， OD的时候填写订单id， A_BB_B的时候填写拍场id
                'payFor': payFor,  # 支付申请类型（OD：orderProcess<申请支付订单>，CG：financeProcess<申请充值>， A_BB_B<延时拍保证金>）
                'payType': payType  # 支付类型（AC：余额账户，AL：支付宝，WX：微信，OF：线下，CM：佣金）
                }
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 支付
    def accountPay_420(self, applyTxnNum, payPassword):
        url = self.host + 'interface/mobile/accountPay_420'
        data = {"applyTxnNum":applyTxnNum, "payPassword":MD5_encryption().md5(payPassword)}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    def changePassword_112(self, oldPwd, type, newPwd):
        url = self.host + 'interface/mobile/changePassword_112'
        data = {"oldPwd": oldPwd, "type": type, "newPwd": MD5_encryption().md5(newPwd)}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
        return req

    # 支付结果
    def payQuery_112(self, applyTxnNum, payType):
        url = self.host + 'interface/mobile/payQuery_112'
        data = {"applyTxnNum":applyTxnNum, "payType": payType}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers,timeout=self.timeout)
        return req

    # 获取广告
    def findAdvertiseContent_260(self, position, deviceType="ANY_TYPE"):
        """
        :param deviceType: ANY_TYPE：任意纵横比;AR_3_2：纵横比3:2;AR_4_3：纵横比4:3;AR_16_9：纵横比16:9
        :param position: P1:拍场广告(已经无效);P2：精品广告（android暂时使用 P1代替）,P3：开机广告;P4：首页顶部广告;
        P5：首页中下部运营广告;P6：精选页广告;P9：门派广告
        :return:
        """
        url = self.host + 'interface/mobile/pmall/findAdvertiseContent_260'
        data = {"deviceType": deviceType, "position": position}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 点赞列表页
    def findUpvoteListByProductId_500(self, productId):
        url = self.host + 'interface/mobile/pmall/findUpvoteListByProductId_500'
        data = {"productId": productId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查询全部宝贝分享信息
    def findCategoryProductShareInfo_500(self, shopId):
        url = self.host + 'interface/mobile/pmall/findCategoryProductShareInfo_500'
        data = {"shopId": shopId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def getMemberDetailInfo_112(self):
        url = self.host + 'interface/mobile/getMemberDetailInfo_112'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 收藏的商品列表
    def findMemberFavoritePage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMemberFavoritePage_500'
        data = {"page": page, "rows": rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 首页查看轰啪拍场
    def findExquisiteAuctionList_260(self):
        url = self.host + 'interface/mobile/pmall/findExquisiteAuctionList_260'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 首页查看秒啪
    def findExquisiteDelayAucAuctionList_430(self):
        url = self.host + 'interface/mobile/pmall/findExquisiteDelayAucAuctionList_430'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 猜你喜欢
    def recommendLotList_420(self):
        url = self.host + 'interface/mobile/pmall/recommendLotList_420'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 查看拍品详情
    def findLotComplex_440(self, lotId):
        url = self.host + 'interface/mobile/pmall/findLotComplex_440'
        data = {"lotId": lotId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 商家详情信息
    def getSellerCalcInfo_400(self, MemberId):
        url = self.host + 'interface/mobile/pmall/getSellerCalcInfo_400'
        data = {"memberId": MemberId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 商家中心--轰啪拍场信息
    def findApprovedAuctionByPage_230(self, memberId, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/findApprovedAuctionByPage_230'
        data = {"memberId":memberId, "page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 商家中心--秒啪拍场信息
    def findDelayAucAuctionPage_420(self, memberId, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/findDelayAucAuctionPage_420'
        data = {"memberId":memberId, "page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 添加评论
    def addLotComment_112(self, memberId, lotId, content):
        url = self.host + 'interface/mobile/addLotComment_112'
        data = {"content": content, "memberId": memberId, "lotId": lotId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看轰啪拍场详情
    def findAuctionDetail(self, auctionId):
        url =self.host+'interface/mobile/pmall/findAuctionDetail_440'
        data = {"auctionId": auctionId}
        req = requests.post(url, data=data, headers=self.headers,timeout=self.timeout)
        return req

    def manualAuctionRegister_230(self, auctionId):
        url = self.host+'interface/mobile/manualAuctionRegister_230'
        bidbond = self.findAuctionDetail(auctionId).json().get('minBidBondAmount')
        data = {"auctionId": auctionId, "expectBidBond":bidbond}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url,data=data,headers=self.headers,timeout=self.timeout)
        return req

    def autoAuctionRegister_230(self, auctionId):
        url = self.host + 'interface/mobile/autoAuctionRegister_230'
        data = {"auctionId": auctionId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def refreshBidInfo_440(self, auctionId, lotId=1, scene="image"):
        url = self.host + 'interface/mobile/refreshBidInfo_440'
        data = {"auctionId": auctionId, "lotId": lotId, "scene": "image"}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findAuctionLotList_260(self, auctionId):
        url = self.host + 'interface/mobile/pmall/findAuctionLotList_260'
        data = {"auctionId": auctionId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findLotComplex_260(self, lotId):
        url = self.host + 'interface/mobile/pmall/findLotComplex_260'
        data = {"lotId": lotId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def enterAuction_270(self, auctionId, avatarType="NICKNAME"):
        url = self.host + 'interface/mobile/enterAuction_270'
        data = {"auctionId": auctionId, "avatarType": avatarType}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def generatePaddleNum_230(self, auctionId):
        url = self.host + 'interface/mobile/generatePaddleNum_230'
        data = {"auctionId": auctionId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 是否开始直播
    def isAuctionLiveStarted_400(self, auctionId):
        url = self.host + 'interface/mobile/isAuctionLiveStarted_400'
        data = {"auctionId": auctionId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findMyAuctionMemberList_270(self, lotId):
        url = self.host + 'interface/mobile/findMyAuctionMemberList_270'
        data = {"lotId": lotId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    def findForumGuide(self):
        url = self.host + 'interface/mobile/pmall/findForumGuide'
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    def findLiveDetail_450(self, liveId):
        url = self.host + 'interface/mobile/pmall/findLiveDetail_450'
        data = {'liveId': liveId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 龖竞拍*界面  获取秒啪系统消息
    def getSysDelayMsg_431(self):
        url = self.host + 'interface/mobile/getSysDelayMsg_431'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 龖竞拍*界面  获取秒啪拍场
    def futureDelayAucAuctionPage_430(self, categoryCode=None, page=1, rows=20):
        """
        :param categoryCode: 分类，默认查看全部
        :param page:
        :param rows:
        :return:
        """
        url = self.host + 'interface/mobile/pmall/futureDelayAucAuctionPage_430'
        data = {'categoryCode': categoryCode, 'page': page, 'rows':rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取我的秒啪参怕列表
    def findMyLotPartakePage_432(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMyLotPartakePage_432'
        data = {'page': page, 'rows': rows}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看秒啪历史拍场
    def historyDelayAucAuctionPage_420(self, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/historyDelayAucAuctionPage_420'
        data = {'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 龖*竞拍 获取拍场信息接口
    def futureAuctionList_270(self, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/futureAuctionList_270'
        data = {'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看轰啪历史信息接口
    def historyAuctionList_270(self, page=1, rows=20):
        url = self.host + 'interface/mobile/pmall/historyAuctionList_270'
        data = {'page': page, 'rows': rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看秒啪详情
    def findDelayAucAuctionDetail_420(self, auctionId):
        url = self.host + 'interface/mobile/pmall/findDelayAucAuctionDetail_420'
        data = {'auctionId': auctionId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看秒拍拍品信息
    def findDelayAucAuctionLotPage_420(self, auctionId, page=1, rows=20, order="asc", sort="id"):
        url = self.host + 'interface/mobile/pmall/findDelayAucAuctionLotPage_420'
        data = {'auctionId': auctionId, "page": page, "rows": rows, "order": order, "sort": sort}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 自动报名秒啪接口
    def autoDelayAucAuctionRegister_420(self, auctionId):
        url = self.host + 'interface/mobile/autoDelayAucAuctionRegister_420'
        data = {'auctionId': auctionId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers,timeout=self.timeout)
        return req

    # 手动报名延时拍拍场拍品
    def manualDelayAucAuctionRegister_420(self, auctionId):
        url = self.host + 'interface/mobile/manualDelayAucAuctionRegister_420'
        data = {'auctionId': auctionId}
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, data=data, headers=self.headers,timeout=self.timeout)
        return req

    def hasDelayAucPermit_420(self):
        url = self.host + 'interface/mobile/hasDelayAucPermit_420'
        self.headers.update(Authorization=self.Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req




if __name__ == '__main__':
    req = v5().getMemberDetailInfo_112()
    print((req.text))
