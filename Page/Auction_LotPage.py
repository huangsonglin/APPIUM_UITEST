#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/22 15:59'

import os,sys
import time
import re,random
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from API.new_500 import *
from API.Order500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Page.AboutLogin import *
from Until.YamlRead import *
from Page.AboutLogin import *
from Page.SellerPage import *
from Page.PulicClass import *

'''
@description:   轰啪-拍品详情页的部分信息校验
'''

class AuctionLotPage:

    defultList = ['微博', '微信', '朋友圈', '龖江湖']

    # 验证拍品详情页的activity是否满足预期
    def Assert_Activity(self, driver):
        try:
            driver.implicitly_wait(10)
            time.sleep(1)
            assert driver.current_activity == '.activity.LotDetailNewActivity'
            cmd(driver).up_swipe()
            time.sleep(1)
            Title = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'title_title_text_view')))
            assert Title.text == '拍品详情'
            cmd(driver).down_swipe()
        except:
            print(f'轰啪拍品详情页和预期结果不一致')
            assert True == False

    def ShareTest(self, driver, channel):
        if channel in self.defultList:
            if channel == '微博':
                PulicClass().ShareIntoWebio(driver)
            elif channel == '微信':
                PulicClass().ShareIntoWeiXin(driver)
            elif channel == '朋友圈':
                PulicClass().ShareIntoWeiXinQuan(driver)
            else:
                PulicClass().ShareIntoDAJIANGHU(Driver)
        else:
            text = f'分享渠道不正确， 请输入{self.defultList}中的渠道'
            raise text

    # 拍拍详情信息验证
    def Lot_Information(self, driver, LotId):
        try:
            LotReq = v5().findLotComplex_440(LotId)
            assert LotReq.status_code == 200
            Name = LotReq.json()['name']
            sellerNickname = LotReq.json()['sellerNickname']
            # 拍品名字
            AppName = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'lot_name_tv')))
            # 拍品卖家
            AppSellNickName = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'tv_nickname')))
            assert AppName.text == Name
            assert AppSellNickName.text == sellerNickname
            # 拍品围观次数
            AppOb = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'observer_count_tv')))
            assert int(AppOb.text) + 1 == int(LotReq.json()['observerCount'])
            # 市场估价
            Market_price = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'tv_market_price_value')))
            MaketText = (Market_price.text[6:].replace(',',''))
            assert MaketText == str((LotReq.json()['marketPriceValue'])).replace(',','')
            # 加价幅度
            bidIncValue = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'tv_bid_inc_value')))
            bidIncValue = float(str(bidIncValue.text).split('¥')[1].replace(',', ''))
            assert bidIncValue == float(LotReq.json()['bidIncValue'])
            # 出价次数
            bidding_price = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'bidding_price_count_tv')))
            bidding_price = (bidding_price.text)[6:]
            assert bidding_price == LotReq.json()['biddingPriceCount']
            begin_price = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'begin_price_tv')))
            begin_price = str(begin_price.text).split('¥')[1].replace(',', '').strip()
            assert float(begin_price) == float(LotReq.json()['beginPrice'])
            [cmd(driver).up_swipe() for k in range(3)]
            time.sleep(1)
            # 其他拍品
            OtherLotList = driver.find_elements_by_xpath('//*[contains(@resource-id, "lot_detail_other_name_tv")]')
            for OtherLot in OtherLotList:
                OtherName = LotReq.json()['otherLotList'][OtherLotList.index(OtherLot)]['name']
                assert OtherLot.text == OtherName
                OtherLot.click()
                driver.implicitly_wait(5)
                self.Assert_Activity(driver)
                driver.back()
                time.sleep(1)
                [cmd(driver).up_swipe() for k in range(3)]
            time.sleep(1)
            [cmd(driver).down_swipe() for k in range(3)]
        except:
            assert True == False

    # 点赞信息验证
    def LotLike(self, driver, LotId):
        time.sleep(2)
        RQ = v5().findLotComplex_440(LotId)
        LikeNum = int(RQ.json()['upvoteCount'])
        [cmd(driver).up_swipe() for k in range(2)]
        # 点赞按钮
        LikeButton = WebDriverWait(driver, timeout=10).until\
            (EC.visibility_of_element_located((By.ID, "tv_member_count")))
        if LikeNum == 0:
            try:
                Toast = WebDriverWait(driver, timeout=10).until\
                    (EC.visibility_of_element_located((By.ID, 'upvote_notice_tv')))
                assert '快来点个赞吧' in str(Toast.text)
                assert LikeNum.text == '赞'
                LikeButton.click()
                time.sleep(1)
                assert LikeButton.text == '1'
                WebDriverWait(driver, timeout=10).until \
                    (EC.visibility_of_element_located((By.ID, 'iv_avatar')))
                LikeButton.click()
                time.sleep(1)
                assert LikeNum.text == '赞'
                WebDriverWait(driver, timeout=10).until \
                    (EC.visibility_of_element_located((By.ID, 'upvote_notice_tv')))
                print(f'初始无点赞时：拍品详情页点赞-取消点赞前端界面存在问题')
            except:
                print(f'初始无点赞时：拍品详情页点赞-取消点赞前端界面正常显示')
                assert True == False
        else:
            try:
                assert LikeButton.text == str(LikeNum)
                LikeButton.click()
                time.sleep(1)
                assert LikeButton.text == str(LikeNum + 1)
                LikeButton.click()
                time.sleep(1)
                assert LikeButton.text == str(LikeNum)
                print(f'已有点赞：拍品详情页点赞-取消点赞前端界面存在问题')
            except:
                assert True == False

    # 评论
    def Comment(self, driver, LotId):
        time.sleep(2)
        RQ = v5().findLotComplex_440(LotId)
        Count = int(RQ.json()['commentCount'])
        [cmd(driver).up_swipe() for k in range(2)]
        try:
            InputText = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.ID, "lot_detail_comment_input_view")))
            TotalText = WebDriverWait(driver, timeout=10).until \
                (EC.visibility_of_element_located((By.ID, "tv_total_comment")))
            Total = ''.join(re.findall('\d', TotalText.text))
            assert Total == str(Count)
            InputText.click()
            time.sleep(1)
            InputBox = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.ID, "lot_detail_comment_input_editText")))
            SendButton = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.ID, "lot_detail_send_reply_button")))
            Area = PulicClass().Chinese(20)
            InputBox.clear()
            time.sleep(1)
            InputBox.send_keys(Area)
            SendButton.click()
            driver.implicitly_wait(10)
            time.sleep(1)
            AftetTotal = ''.join(re.findall('\d', TotalText.text))
            assert Total == str(Count + 1)
            ContentText = driver.find_elements_by_id('tv_content')[0]
            assert ContentText.text == Area
        except:
            print(f'用户添加评论功能存在问题，请及时手动验证')
            assert True == False

    # 竞拍须知
    def IntoNotice(self, driver, LotId):
        try:
            [cmd(driver).up_swipe() for k in range(2)]
            ELE = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '竞拍须知')]")))
            ELE.click()
            driver.implicitly_wait(2)
            time.sleep(2)
            assert driver.current_activity == '.activity.WebViewActivity'
            Title = WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located
                                                           ((By.ID, "tv_title")))
            assert Title.text == '竞拍须知'
            driver.back()
        except:
            assert True == False

    # 付款须知
    def IntoPayNotice(self, driver):
        try:
            [cmd(driver).up_swipe() for k in range(2)]
            ELE = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '付款须知')]")))
            ELE.click()
            driver.implicitly_wait(2)
            time.sleep(2)
            assert driver.current_activity == '.activity.WebViewActivity'
            Title = WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located
                                                           ((By.ID, "tv_title")))
            assert Title.text == '付款须知'
            driver.back()
        except:
            assert True == False

    # 点击进入卖家信息页面
    def Into_seller(self, driver, LotId):
        try:
            RQ = v5().findLotComplex_440(LotId)
            sellerId = RQ.json()['sellerId']
            [cmd(driver).down_swipe() for k in range(2)]
            INTOBUTTON = WebDriverWait(driver, timeout=10).until \
                (EC.visibility_of_element_located((By.ID, 'btn_store_in')))
            assert INTOBUTTON.text == '商家中心'
            INTOBUTTON.click()
            driver.implicitly_wait(5)
            time.sleep(1)
            SellerPage().AssertINIT(driver, sellerId)
            time.sleep(1)
            SellerPage().IntoMessage(driver, sellerId)
            time.sleep(1)
            SellerPage().IntoPersonalPage(driver, sellerId)
            time.sleep(1)
            SellerPage().productList(driver, sellerId)
            time.sleep(1)
            SellerPage().DelayAuction(driver, sellerId)
            time.sleep(1)
            SellerPage().Auction(driver, sellerId)
            driver.back()
        except:
            assert True == False



