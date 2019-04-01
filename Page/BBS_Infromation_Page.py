#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/28 14:15'

import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import random,re
import time, datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import math
from Page.PulicClass import *
from Command.command import command as cmd
from API.BBS500 import *
from API.V5down import *

class BBS_Imfromation:

    # 查看初始信息
    def check_init_status(self, driver, postId):
        try:
            Dreq = V5_BBS().findPostDetailInfo_300(postId)
            if Dreq.status_code == 200:
                assert driver.current_activity == ".activity.RiversLakesTopicDetailActivity", u'BBS详情界面activity正确'
                page_title = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/tv_title")')
                assert page_title.text == '话题详情'
                # 发帖者头像icon
                icon = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/topic_detail_iv_avatar")')
                # 关注按钮
                focus_button = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/exquitste_topic_detail_focus")')
                # 评论框
                content_box = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/rivers_lakesdetail_comment_input_view")')
                # 收藏按钮
                like_button = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/topic_detail_bottom_collection_im")')
                his_other_bbs_req = V5_BBS().findCurrentPublishPostPage_300(postId)
                if his_other_bbs_req.status_code == 200 and his_other_bbs_req.json()['total'] != "0":
                    loc = (By.XPATH, "//*[contains(@text, 'Ta最近的发布')]")
                    PulicClass().up_swipe_to_display(driver, *loc)
                his_connect_bbs_req = V5_BBS().findRecommendPostList_300(postId)
                if his_connect_bbs_req.status_code == 200 and len(his_connect_bbs_req.json()) > 0:
                    connectloc = (By.XPATH, "//*[contains(@text, '相关推荐')]")
                    PulicClass().up_swipe_to_display(driver, *connectloc)
                LikeLoc = (By.ID, "cn.dcpai.auction:id/river_lake_topic_detail_member_count_tv")
                PulicClass().up_swipe_to_display(driver, *LikeLoc)
            else:
                Error = Dreq.json()['globalErrors']
                Toast = PulicClass().Toast(driver, Error)
                assert Toast == True
            [cmd(driver).down_swipe() for i in range(4)]
        except:
            print(f'BBS详情界面存在一定的问题，请及时手动查看~~~')
            PulicClass().save_img(driver, 'BBS_Infromation_InitPage')

    # 查看详细信息
    def check_detail_information(self, driver, postId):
        Dreq = V5_BBS().findPostDetailInfo_300(postId)
        if Dreq.status_code > 200:
            print(f'当前BBS无法正常查看，因为{Dreq.json()["globalErrors"]}')
        else:
            try:
                # 发帖者名字
                Name = driver.find_element_by_android_uiautomator\
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/topic_detail_nickname_tv")')
                assert Name.text in Dreq.json()['memberNickname']
                # 会员等级
                MemberLeval = driver.find_element_by_android_uiautomator\
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/exquitste_topic_detail_iv_level")')
                assert ''.join(re.findall('\d', MemberLeval.text)) == Dreq.json()['memberLevel']
                TypeList = []
                for result in Dreq.json()['postContentList']:
                    TypeList.append(result['mediaType'])
                # 详情内容不好判断--后期做详细划分
                # 发布时间
                PushTimeLoc = (By.ID, "cn.dcpai.auction:id/topic_detail_header_publish_time_tv")
                PulicClass().up_swipe_to_display(driver, *PushTimeLoc)
                # 时间显示规则需要重定义
                PushTime = WebDriverWait(driver, 2).until(EC.visibility_of_element_located(PushTimeLoc))
                # assert PushTime.text == Dreq.json()['publishTime'].split(' ')[0]
                observercount = driver.find_element_by_id('cn.dcpai.auction:id/topic_detail_header_observercount_tv')
                # assert observercount.text == Dreq.json()['observercount'] # 围观信息未及时刷新，存在缓存
                # 评论
                CommentLoc = (By.ID, "cn.dcpai.auction:id/river_lake_topic_detail_total_comment_tv")
                PulicClass().up_swipe_to_display(driver, *CommentLoc)
                CommentTotal = WebDriverWait(driver, 2).until(EC.visibility_of_element_located(CommentLoc))
                Creq = V5_BBS().findTopReplyByPostId_300(postId)
                assert ''.join(re.findall('\d', CommentTotal.text)) == Creq.json()['total']
                # 点赞人数及点赞按钮
                upvoteCount = driver.find_element_by_id('cn.dcpai.auction:id/river_lake_topic_detail_member_count_tv')
                if Dreq.json()['upvoteCount'] == '0':
                    assert upvoteCount.text == '赞'
                else:
                    assert ''.join(re.findall('\d', upvoteCount.text.replace(',', ''))) == Dreq.json()['upvoteCount']
            except:
                assert True == False
                print(f'帖子详情内容可能存在问题，请及时手动查看')

    # 评论帖子
    def check_comment_bbs(self, driver, postId):
        FristReq = Down_V5Api().findTopReplyByPostId_300(postId)
        FristNum = int(FristReq.json()['total'])
        try:
            CommentBox = WebDriverWait(driver, 2).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/rivers_lakesdetail_comment_input_view")))
            CommentBox.click()
            TextInputBox = WebDriverWait(driver, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/topic_detail_comment_input_view")))
            TextInputBox.clear()
            CommentText = PulicClass().Chinese(30)
            TextInputBox.send_keys(CommentText)
            SendButton = driver.find_element_by_id('cn.dcpai.auction:id/topic_detail_send_reply_button')
            SendButton.click()
            try:
                assert PulicClass().new_toast(driver, "评论成功") == True
            except:
                pass
            SecondReq = Down_V5Api().findTopReplyByPostId_300(postId)
            SecondNum = int(SecondReq.json()['total'])
            difference_value = FristNum - SecondNum
            print(difference_value)
            [cmd(driver).up_swipe() for i in range(SecondNum)]
            time.sleep(1)
            LastComment = driver.find_elements_by_id\
                ('cn.dcpai.auction:id/river_lakes_comment_content_tv')[difference_value].text
            assert LastComment == CommentText
            TopButton = driver.find_element_by_id('cn.dcpai.auction:id/top_view_img')
            TopButton.click()
        except:
            print(f'评论帖子功能可能存在问题，请及时手动查看')



