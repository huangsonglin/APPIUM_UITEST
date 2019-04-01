#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/26 16:33'

"""
__Description__: 主要针对轰啪拍场做正确性验证
"""

import os,sys
import time
import re,random
from Until.YamlRead import *
from Command.command import command as cmd
from appium.webdriver import webdriver
from appium.webdriver.webelement import WebElement
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from API.new_500 import *
from API.BBS500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import *
from Page.AboutLogin import *
from Page.AboutLogin import *
from Page.SellerPage import *
from Page.PulicClass import *
from Page.Pay_Margin import *
from Page.ImageView_Living import *
from Page.IM import *
from Page.SellerPage import *


class AuctionPage:

    # driver = Driver().get_driver()
    # 轰啪拍场初始化界面信息验证
    def INITAssert(self, driver, AuctionId):
        try:
            RQ = v5().findAuctionDetail(AuctionId)
            AuctionName = RQ.json()['name']     # 拍场名字
            DESC = RQ.json()['desc']            # 拍场描述
            lotCount = RQ.json()['lotCount']    # 拍场拍品数量
            minBidBondAmount = RQ.json()['minBidBondAmount']    # 拍场保证金
            memberNickname = RQ.json()['memberNickname']    # 卖家
            AuctionStatus = RQ.json()['auctionState']
            AuctionList = []
            CollectAuction = V5_BBS().findMyFavoriteAuctionPage_500()
            for result in CollectAuction.json()['rows']:
                AuctionList.append(result['id'])
            driver.implicitly_wait(10)
            time.sleep(2)
            assert driver.current_activity == '.activity.AuctionGroupDetailNewActivity'
            AName = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, "title_title_text_view")))
            assert AName.text == AuctionName
            SellName = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "tv_nickname")))
            assert (SellName.text).replace('...','') in memberNickname
            AppLotNum = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "lot_count_tv")))
            assert ''.join(re.findall('\d', AppLotNum.text)) == lotCount
            AppbondMoney = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "no_specially_bond_amount_tv")))
            assert float(''.join(re.findall('\d',str(AppbondMoney.text).replace(',','')))) == float(minBidBondAmount)
            TIME = AppbondMoney = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "start_time_tv")))
            if AuctionStatus == 'A':
                assert '距结束' in TIME.text
            else:
                assert (TIME.text)[-5:] == RQ.json()['startTime'][-8:-3]
            CollectButton = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'title_favorite_check_box')))
            assert CollectButton.get_attribute('clickable') == 'true' # 可点击性
            # 收藏状态验证
            if str(AuctionId) in AuctionList:
                assert CollectButton.get_attribute('checked') == "true"
                CollectButton.click()
                time.sleep(1)
                assert CollectButton.get_attribute('checked') == "false"
            else:
                assert CollectButton.get_attribute('checked') == "false"
                CollectButton.click()
                time.sleep(1)
                assert CollectButton.get_attribute('checked') == "true"
        except:
            assert True == False

    # 商家中心
    def Into_SellCenter(self, driver, auctionId):
        try:
            Rq = v5().findAuctionDetail(auctionId)
            SellId = Rq.json()['memberId']
            loc = (By.ID, "cn.dcpai.auction:id/btn_go_shop")
            SellCenter = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(loc))
            SellCenter.click()
            time.sleep(2)
            driver.implicitly_wait(10)
            SellerPage().AssertINIT(driver, SellId)
            SellerPage().Auction(driver, SellId)
            SellerPage().DelayAuction(driver, SellId)
            SellerPage().productList(driver, SellId)
            driver.back()
            time.sleep(1)
        except:
            pass
            print(f'从拍场界面进入商家中心页面后，商家中心页面存在问题~~~~')

    # 用户自动报名成功与否前端展示验证
    def userAutoResiter(self, driver, auctionId):
        try:
            ARQ = v5().findAuctionDetail(auctionId)
            if 'liveAuctioneerId' in list(ARQ.json().keys()):
                liveAuctioneerId = ARQ.json()['liveAuctioneerId']   # 主播账号
            else:
                liveAuctioneerId = None
            auctioneerId = ARQ.json()['auctioneerId']   # 拍卖师
            sellId = ARQ.json()['memberId']             # 卖家
            AuctionState = ARQ.json()['auctionState']
            minBidBondAmount = int(float(ARQ.json()['minBidBondAmount']))
            MYQ = v5().getMemberDetailInfo_112()
            MyNum = MYQ.json()['id']
            MyName = MYQ.json()['name']
            AUTORQ = v5().autoAuctionRegister_230(auctionId)
            # 拍场未结束和未提前入场的状态
            if AuctionState in ['A', 'S', 'P']:
                assert AUTORQ.status_code == 200
                Result = AUTORQ.json()['registered']
                # 自动报名失败者当前验证
                if Result == False:
                    try:
                        # 进场围观按钮
                        OnlookButton = WebDriverWait(driver, timeout=3).until \
                            (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '进场围观')]")))
                        OnlookButton.click()
                        time.sleep(2)
                        assert driver.current_activity in \
                               ['.activity.AuctionNewActivity', '.auction.auction.AuctionActivity']
                        if driver.current_activity == '.activity.AuctionNewActivity':
                            IM().Price_switch_IM(driver)
                            IM().send_text(driver)
                            IM().send_emoij(driver)
                            IM().send_image(driver)
                            IM().IM_switch_Price(driver)
                            AuctionLive_ImageView().look_lot(driver, auctionId)
                            AuctionLive_ImageView().onlooker_price(driver, auctionId)
                        PulicClass().quit_auction(driver)
                        time.sleep(2)
                        # 进入拍卖现场
                        IntoLive = WebDriverWait(driver, timeout=3).until \
                            (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '我要竞拍')]")))
                        IntoLive.click()  # 点击我要竞拍--进入缴纳保证金界面
                        PayMargin().Assert_INIT(driver, auctionId)
                        PayMargin().PayMethod(driver)
                    except:
                        assert True == False
                else:
                    if MyNum != sellId or MyNum != auctioneerId or MyNum != liveAuctioneerId:
                        INTOPirce = WebDriverWait(driver, timeout=3).until\
                            (EC.visibility_of_element_located((By.ID, 'enough_bond_join_auction_btn')))
                        INTOPirce.click()
                        time.sleep(2)
                        driver.implicitly_wait(10)
                        try:
                            # 自动报名成功后当前界面的提示信息
                            Toast = WebDriverWait(driver, timeout=5).until\
                                (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text,"知道了")]')))
                            Toast.click()
                        except:
                            pass
                        # 进入入场准备界面
                        if driver.current_activity == '.activity.AdmissionReadyNewActivity':
                            assert WebDriverWait(driver, timeout=3).until\
                                (EC.visibility_of_element_located((By.ID, "tv_title"))).text == '入场准备'
                            # 默认实名
                            RealNameTAG = WebDriverWait(driver, timeout=3).until\
                                (EC.visibility_of_element_located((By.ID, "real_name_ImageView")))
                            REALNAME = WebDriverWait(driver, timeout=3).until \
                                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '实名参拍')]")))
                            NAMETEXT = WebDriverWait(driver, timeout=3).until \
                                (EC.visibility_of_element_located((By.ID, "tv_real_name")))
                            assert NAMETEXT.text == MyName
                            Anonymity = WebDriverWait(driver, timeout=3).until \
                                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '匿名参拍')]")))
                            RefreshNum = WebDriverWait(driver, timeout=3).until \
                                (EC.visibility_of_element_located((By.ID, "refresh_ImageView")))
                            RandomNum = WebDriverWait(driver, timeout=3).until \
                                (EC.visibility_of_element_located((By.ID, "tv_number")))
                            NUM_ONE = RandomNum.text
                            assert RefreshNum.is_enabled() == False
                            Anonymity.click()
                            assert RefreshNum.is_enabled() == True
                            RefreshNum.click()
                            time.sleep(1)
                            NUM_TWO = RandomNum.text
                            assert NUM_ONE != NUM_TWO, u'匿名刷新功能正常'
                            REALNAME.click()
                            ImageLive = WebDriverWait(driver, timeout=3).until\
                                (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text,"文字拍场")]')))
                            ImageLive.click()
                        try:
                            AuctionLive_ImageView().look_lot(driver, auctionId)
                        except:
                            pass
                        try:
                            AuctionLive_ImageView().successPrice(driver, auctionId, 1250503)
                        except:
                            pass
                        try:
                            IM().Price_switch_IM(driver)
                        except:
                            pass
                        try:
                            IM().send_text(driver)
                        except:
                            pass
                        try:
                            IM().send_emoij(driver)
                        except:
                            pass
                        try:
                            IM().send_image(driver)
                        except:
                            pass
                        try:
                            PulicClass().quit_auction(driver)
                        except:
                            pass
            else:
                assert AUTORQ.status_code > 200
                self.INITAssert(driver, auctionId)
                print(f'当前拍场{auctionId}未开始，跳过该case')
        except:
            assert True == False

    # 分享拍场
    def Auction_Share(self, driver, channel):
        defultList = ['微博', '微信', '朋友圈', '龖江湖']
        if channel in defultList:
            if channel == '微博':
                PulicClass().ShareIntoWebio(driver)
            elif channel == '微信':
                PulicClass().ShareIntoWeiXin(driver)
            elif channel == '朋友圈':
                PulicClass().ShareIntoWeiXinQuan(driver)
            else:
                PulicClass().ShareIntoDAJIANGHU(Driver)
        else:
            text = f'分享渠道不正确， 请输入{defultList}中的渠道'
            raise text

    # 查看拍品相关信息
    def Find_AuctionLot(self, driver, auctionId):
        try:
            REQ = v5().findAuctionLotList_260(auctionId)
            loc = (By.XPATH, "//*[contains(@resource-id,'iv_avatar')]")
            PulicClass().up_swipe_to_display(driver, *loc)
            NUM = len(REQ.json())
            # 卖家头像
            Icon = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(loc))
            # 拍场描述、
            Desc = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'auction_desc_tv')]")))
            # 返回按钮
            back_button = driver.find_element_by_id('cn.dcpai.auction:id/title_back_btn')
            back_bar = driver.find_element_by_id('back_title_favorite_share_title_bar')
            Y = PulicClass().get_box(driver, back_bar)[3] - PulicClass().get_box(driver, back_bar)[1]
            driver.drag_and_drop(Desc, back_bar)
            time.sleep(1)
            PulicClass().randow_hight_swipe(driver, Y)
            for i in range(NUM):
                if i < NUM-1:
                    lotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/auction_item_LinearLayout')
                    lotName = lotRoot[0].find_element_by_id('cn.dcpai.auction:id/lot_name_tv')
                    lotTime = lotRoot[0].find_element_by_id('cn.dcpai.auction:id/tv_time')
                    M = PulicClass().get_box(driver, lotTime)[3] - PulicClass().get_box(driver, lotName)[1]
                    PulicClass().randow_hight_swipe(driver, M)
                    assert lotName.text == REQ.json()[i]['name'], u'拍品名字一致'
                    NowDate = datetime.datetime.now().date()
                    ReqTime = REQ.json()[i]['startTime']
                    LotStatus = REQ.json()[i]['auctionState']
                    # 表示开始时间为当前系统时间日期
                    if str(NowDate) in ReqTime:
                        lotTimeText = '今天 ' + ReqTime.split(' ')[1][0:-3]
                    else:
                        lotTimeText = ReqTime[5:-3]
                        lotTimeText = lotTimeText.replace('-', '月').split(' ')
                        lotTimeText = lotTimeText[0] + '日 ' + lotTimeText[1]
                    if LotStatus in ['N', 'F']:
                        if LotStatus == 'N':
                            lotTimeText = lotTimeText + ' 开始'
                        assert lotTime.text == lotTimeText, u'拍品开始时间和接口一致'
                    else:
                        assert '距结束' in lotTime.text
                    # 围观情况
                    lotOb = lotRoot[0].find_element_by_id('cn.dcpai.auction:id/observer_count_tv')
                    assert ''.join(re.findall('\d', str(lotOb.text).replace(',', ''))) == \
                           REQ.json()[i]['observerCount'], u'拍品围观次数和接口一致'
                    # 起拍价|成交价
                    lotBeginPrice = lotRoot[0].find_element_by_id('cn.dcpai.auction:id/begin_price_tv')
                    assert float(''.join(re.findall('\d', str(lotBeginPrice.text).replace(',', '')))) == \
                           float(REQ.json()[i]['beginPrice']), u'拍品起拍价|成交价|当前价和接口一致'
                    # 市场估价
                    lotMarketPrice = lotRoot[0].find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
                    assert str(lotMarketPrice.text).split(':')[1].strip() == \
                           REQ.json()[i]['marketPriceValue'], u'拍品市场估价和接口数据一致'
                    # 点赞人数
                    LikeTotalMember = driver.find_element_by_id('cn.dcpai.auction:id/tv_member_count_text')
                    original_upvoteCount = REQ.json()[i]['upvoteCount']
                    # 点赞按钮
                    LikeButton = driver.find_element_by_id("cn.dcpai.auction:id/tv_member_count_img")
                    try:
                        is_upvote = REQ.json()[i]['upvote']
                        if int(original_upvoteCount) == 0:
                            assert LikeTotalMember.text == '赞'
                            assert is_upvote == False
                            LikeButton.click()
                            ALikeTotalMember = driver.find_element_by_id('cn.dcpai.auction:id/tv_member_count_text')
                            assert ALikeTotalMember.text == '1'
                            LikeButton.click()
                            time.sleep(1)
                            assert driver.find_element_by_id('cn.dcpai.auction:id/tv_member_count_text').text == '赞'
                        else:
                            assert ''.join(re.findall('\d', str(LikeTotalMember.text).replace(',', ''))) == \
                                   original_upvoteCount
                            if is_upvote:
                                LikeButton.click()
                                time.sleep(1)
                                ALikeTotalMember = driver.find_element_by_id('cn.dcpai.auction:id/tv_member_count_text')
                                if int(original_upvoteCount) > 1:
                                    assert int(ALikeTotalMember.text) + 1 == int(original_upvoteCount)
                                else:
                                    assert ALikeTotalMember.text == '赞'
                            else:
                                LikeButton.click()
                                time.sleep(1)
                                ALikeTotalMember = driver.find_element_by_id('cn.dcpai.auction:id/tv_member_count_text')
                                assert int(ALikeTotalMember.text) - 1 == int(original_upvoteCount)
                    except:
                        print(f'拍品点赞功能存在问题，请测试相关人员及时查看~~~~')
                        pass
                    # 点赞会员头像父级
                    members_LinearLayout = driver.find_element_by_id("auction_detail_members_LinearLayout")
                    driver.drag_and_drop(members_LinearLayout, back_button)
                    time.sleep(1)
                    PulicClass().randow_hight_swipe(driver, M)
                else:
                    lotName = driver.find_elements_by_id('cn.dcpai.auction:id/lot_name_tv')
                    assert lotName[-1].text == REQ.json()[i]['name'], u'最后一件拍品名字和接口一致'
                    # 围观情况
                    lotOb = driver.find_elements_by_id('cn.dcpai.auction:id/observer_count_tv')
                    assert ''.join(re.findall('\d', str(lotOb[-1].text).replace(',', ''))) == \
                           REQ.json()[i]['observerCount'], u'拍品围观次数和接口一致'
                    # 起拍价|成交价
                    lotBeginPrice = driver.find_elements_by_id('cn.dcpai.auction:id/begin_price_tv')
                    assert float(''.join(re.findall('\d', str(lotBeginPrice[-1].text).replace(',', '')))) == \
                           float(REQ.json()[i]['beginPrice']), u'拍品起拍价|成交价|当前价和接口一致'
                    # 市场估价
                    lotMarketPrice = driver.find_elements_by_id('cn.dcpai.auction:id/tv_market_price_value')
                    assert str(lotMarketPrice[-1].text).split(':')[1].strip() == REQ.json()[i]['marketPriceValue'], u'拍品市场估价和接口数据一致'
        except:
            print(f'查看当前拍场中的每件拍品详情可能存在问题，请测试人员及时手动复查~~~~')
            assert True == False










