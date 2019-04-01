#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2018/12/6 13:58'


import os
import requests
import random
import time
import hashlib
from urllib import parse
from Until.YamlRead import *


class V5_BBS:
    host = 'http://testapp.dcpai.cn/app/'
    headers = {'User-Agent': 'Auction/5.0.0 (iPhone; ANDROID 11.4.1; Scale/2.00)',
               'Accept-Language': 'zh-Hans-CN;q=1',
               'Connection': 'keep-alive',
               'Content - Type': 'application/x-www-form-urlencoded',
               'clientType': 'ANDROID'}
    timeout = 3
    Authorization = Config(App_LoginToken).get('Authorization')

    # 统计用户 话题 评论  关注  粉丝 点赞 门派 收藏 积分数据
    def findCount_500(self):
        url = self.host + 'interface/mobile/findCount_500'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 龘江湖-收藏-商品
    def findMemberFavoritePage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMemberFavoritePage_500'
        Authorization = self.Authorization
        data = {'page':page , 'rows':rows}
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 龘江湖-收藏-拍场
    def findMyFavoriteAuctionPage_500(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMyFavoriteAuctionPage_500'
        Authorization = self.Authorization
        data = {'page':page , 'rows':rows}
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 发帖
    def addPost_300(self):
        url = self.host + 'interface/mobile/addPost_300'
        Authorization = self.Authorization
        Content = ''
        for i in range(20):
            name = chr(random.randint(0x4E00, 0x9FBF))
            Content = Content + name
        data = {'attachmentType': 'IMAGE',
                'postContentList':
                    [{'mediaType': 'TEXT', 'content': Content},
                     {'imageWidth': 1280, 'mediaType': 'IMAGE',
                      'imageName': 'C88A20AF-2560-41E6-B213-2C90FEAFF23D0.JPG',
                      'imageHeight': 2272}], 'typeId': 2}
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
        return req

    # 帖子点赞
    def addPostUpvote_200(self, postId):
        url = self.host + 'interface/mobile/addPostUpvote_200'
        data = {"postId": postId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 加入门派
    def joinForum_300(self, forumId):
        url = self.host + 'interface/mobile/joinForum_300'
        data = {"forumId": forumId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 关注|取消关注
    def addOrDeleteFocus_112(self, targetMemberId, focus=1):
        url = self.host + 'interface/mobile/addOrDeleteFocus_112'
        data = {"targetMemberId": targetMemberId, "focus":focus}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 评论帖子
    def addReplyForPost_300(self, postId):
        url = self.host + 'interface/mobile/addReplyForPost_300'
        content = ''
        for i in range(20):
            name = chr(random.randint(0x4E00, 0x9FBF))
            content = content + name
        data = {"content": content, "postId": postId}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 创建门派
    def addForum_300(self, name, icon, declaration):
        url = self.host + 'interface/mobile/addForum_300'
        data = {"name": name, "declaration": declaration, 'icon':icon}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取我的门派
    def findMyForumPage_300(self, page=1, rows=10):
        url = self.host + 'interface/mobile/findMyForumPage_300'
        data = {"page": page, "rows": rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 获取未读消息
    def getUnReadMsgCount_201(self):
        url = self.host + 'interface/mobile/getUnReadMsgCount_201'
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, headers=self.headers, timeout=self.timeout)
        return req

    # 关注的江湖贴
    def findMyFocusMemberPostPage_300(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMyFocusMemberPostPage_300'
        data = {"page": page, "rows": rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 我收藏的帖子
    def findMyFavoritePostPage_300(self, page=1, rows=20):
        url = self.host + 'interface/mobile/findMyFavoritePostPage_300'
        data = {"page": page, "rows": rows}
        Authorization = self.Authorization
        self.headers.update(Authorization=Authorization)
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看帖子详情
    def findPostDetailInfo_300(self, postId):
        url = self.host + 'interface/mobile/pmall/findPostDetailInfo_300'
        data = {"postId": postId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 他最近发布的帖子
    def findCurrentPublishPostPage_300(self, postId):
        url = self.host + 'interface/mobile/pmall/findCurrentPublishPostPage_300'
        data = {"postId": postId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 帖子评论列表
    def findTopReplyByPostId_300(self, postId, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/findTopReplyByPostId_300'
        data = {"postId": postId, "page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 帖子详情页--相关推荐
    def findRecommendPostList_300(self, postId):
        url = self.host + 'interface/mobile/pmall/findRecommendPostList_300'
        data = {"postId": postId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 热门门派
    def findHotForum_300(self, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/findHotForum_300'
        data = {"page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 搜索门派
    def searchForumPage_300(self, keyword, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/searchForumPage_300'
        data = {"keyword": keyword, "page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看门派简单信息
    def findForumSimpleInfo_300(self, forumId):
        url = self.host + 'interface/mobile/pmall/findForumSimpleInfo_300'
        data = {"forumId": forumId}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

    # 查看门派--的全部帖子
    def findForumAllPostPage_300(self, forumId, page=1, rows=10):
        url = self.host + 'interface/mobile/pmall/findForumAllPostPage_300'
        data = {"forumId": forumId, "page": page, "rows": rows}
        req = requests.post(url, data=data, headers=self.headers, timeout=self.timeout)
        return req

if __name__ == '__main__':

    req = V5_BBS().findForumAllPostPage_300(4)
    print(req.text)
