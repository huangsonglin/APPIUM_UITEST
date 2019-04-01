#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/4/1 15:59'

import os,sys
import time
import re, string
from Command.command import command as cmd
from selenium.webdriver.common.by import By
from API.new_500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Page.PulicClass import *
from API.V5down import *
from API.BBS500 import *


class SchoolPage:

    # 查看初始信息
    def check_init_page(self, driver, forumId):
        req = V5_BBS().findForumSimpleInfo_300(forumId)
        try:
            assert driver.current_activity == '.activity.SchoolInfoActivity'
            page_title = driver.find_element_by_id('cn.dcpai.auction:id/title_txt')
            assert page_title.text in req.json()['name']
            name = driver.find_element_by_id('cn.dcpai.auction:id/school_name')
            assert name.text == req.json()['name']
            membertotal = driver.find_element_by_id('cn.dcpai.auction:id/school_member_tv')
            assert ''.join(re.findall('\d', membertotal.text)) == req.json()['memberPage']['total']
            school_describe = driver.find_element_by_id('cn.dcpai.auction:id/school_describe_tv')
            assert ''.join(re.findall('\d', school_describe.text.split('·')[0])) == req.json()['reputation']
            assert ''.join(re.findall('\d', school_describe.text.split('·')[1])) == req.json()['postCount']
        except:
            print(f'查看门派详情页时，相关信息存在问题。请测试人员及时手动查看~~~~')
            PulicClass().save_img(driver, 'school_detail_page')

    # 查看门派全部帖子
    def check_all_postBBS(self, driver, forumId):
        req = V5_BBS().findForumAllPostPage_300(forumId)
        try:
            listtitle = driver.find_elements_by_id('android.support.v7.app.ActionBar$Tab')
            page_title = driver.find_element_by_id('cn.dcpai.auction:id/title_txt')
            driver.drag_and_drop(listtitle[0], page_title)
            listtitle[0].click()

        except:
            print(f'门派详情页，查看全部帖子功能存在问题。请测试人员及时手动查看~~~')
            PulicClass().save_img(driver, 'school_detail_page_look_allbbs')
