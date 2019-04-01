#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/22 17:22'

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



class SellerPage:

    # 商家界面初始化验证
    def AssertINIT(self, driver, sellerId):
        try:
            SellReq = v5().getSellerCalcInfo_400(sellerId)
            assert SellReq.status_code == 200
            NikeName = SellReq.json()['name']  # 卖家Name
            focusNum = SellReq.json()['focus']  # 关注数量
            fansNum = SellReq.json()['fans']  # 粉丝数量
            sellerSoldOutCount = SellReq.json()['sellerSoldOutCount']  # 成交总量笔数
            sellerSoldOutAmount = float(SellReq.json()['sellerSoldOutAmount'])  # 成交总金额
            sellerOdPositiveRate = SellReq.json()['sellerOdPositiveRate']  # 好评率
            sellerOdSuccessRate = SellReq.json()['sellerOdSuccessRate']  # 成交率
            sellerOdReturnRate = SellReq.json()['sellerOdReturnRate']  # 退货率
            assert driver.current_activity == '.activity.OthersStoreActivity'
            # 好评率
            TextView1 = WebDriverWait(driver, 3, 0.5).until\
                (EC.visibility_of_element_located((By.XPATH, '//*[@resource-id="cn.dcpai.auction:id/tv_rate_1"]')))
            # 成交率
            TextView2 = WebDriverWait(driver, 3, 0.5).until\
                (EC.visibility_of_element_located((By.XPATH, '//*[@resource-id="cn.dcpai.auction:id/tv_rate_2"]')))
            # 退货率
            TextView3 = WebDriverWait(driver, timeout=3).until\
                (EC.visibility_of_element_located((By.XPATH, '//*[@resource-id="cn.dcpai.auction:id/tv_rate_3"]')))
            assert str(TextView1.text).split(':')[1].strip() == sellerOdPositiveRate, u'好评率和接口返回数据一致'
            assert str(TextView2.text).split(':')[1].strip() == sellerOdSuccessRate, u'成交率和接口返回数据一致'
            assert str(TextView3.text).split(':')[1].strip() == sellerOdReturnRate, u'退货率率和接口返回数据一致'
            Money = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'tv_money')))
            Count = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'tv_count')))
            assert float(str(Money.text)[0:-1]) == sellerSoldOutAmount, u'成交总额和接口返回数据一致'
            assert float(str(Count.text)[0:-1]) == float(sellerSoldOutCount), u'成交总量和接口返回数据一致'
            driver.implicitly_wait(2)
            TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
            # 卖家有店铺权限
            if v5().getSellerCalcInfo_400(sellerId).json()['hasShop']:
                Num1 = ''.join(re.findall('(\d)', TitleList[0].text))
                Num2 = ''.join(re.findall('(\d)', TitleList[1].text))
                Num3 = ''.join(re.findall('(\d)', TitleList[2].text))
                assert Num3 == v5().findApprovedAuctionByPage_230(sellerId).json()['total'], u'轰啪拍场总数和接口数据一致'
                assert Num2 == v5().findDelayAucAuctionPage_420(sellerId).json()['total'], u'秒啪拍场总数和接口数据一致'
                assert Num1 == v5().myShopAllProductPage_500(sellerId).json()['total'], u'商品总数和接口数据一致'
            else:
                Num1 = ''.join(re.findall('(\d)', TitleList[0].text))
                Num2 = ''.join(re.findall('(\d)', TitleList[1].text))
                assert Num2 == v5().findApprovedAuctionByPage_230(sellerId).json()['total'], u'轰啪拍场总数和接口数据一致'
                assert Num1 == v5().findDelayAucAuctionPage_420(sellerId).json()['total'], u'秒啪拍场总数和接口数据一致'
        except:
            print(f'商家中心界面--初始状态存在问题，请测试人员及时查看~~~~')
            pass

    # 进私信聊天界面
    def IntoMessage(self, driver, sellerId):
        try:
            SellReq = v5().getSellerCalcInfo_400(sellerId)
            assert SellReq.status_code == 200
            NikeName = SellReq.json()['name']  # 卖家Name
            PrivacyMessage = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "私信")]')))
            PrivacyMessage.click()
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.DcChatActivity'
            Name = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'title')))
            assert Name.text[0:-3] in NikeName
            SendButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'et_sendmessage')))
            print(f'进入与卖家私信聊天界面功能正常')
        except:
            print(f'进入与卖家私信聊天界面存在问题')
        driver.back()

    # 进卖家中心界面
    def IntoPersonalPage(self, driver, sellerId):
        try:
            SellReq = v5().getSellerCalcInfo_400(sellerId)
            assert SellReq.status_code == 200
            focusNum = SellReq.json()['focus']  # 关注数量
            fansNum = SellReq.json()['fans']  # 粉丝数量
            PersonalPage = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "personal")))
            assert PersonalPage.text == '个人主页'
            PersonalPage.click()
            time.sleep(2)
            driver.implicitly_wait(5)
            assert driver.current_activity == ".activity.MyJiangHuActivity"
            TitleName = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'tv_nickname')))
            Fans = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'tv_fans_count')))
            Focus = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'tv_focus_count')))
            assert ''.join(re.findall('\d', Fans.text)) == fansNum
            assert ''.join(re.findall('\d', Focus.text)) == focusNum
            MessageButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'letter')))
            FocusButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'focus')))
            StoreButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, 'store')))
            assert MessageButton.text == '私信'
            assert '关注' in FocusButton.text
            assert StoreButton.text == '商家中心'
            print(f'进入卖家个人主页界面功能正常')
        except:
            print(f'进入卖家个人主页界面存在问题')
        driver.back()

    # 商品列表信息展示测试
    def productList(self, driver, sellerId):
        try:
            if v5().getSellerCalcInfo_400(sellerId).json()['hasShop']:
                TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
                TitleList[0].click()
                ProductReq = v5().myShopAllProductPage_500(sellerId)
                if int(ProductReq.json()['total']) == 0:
                    try:
                        Totas = WebDriverWait(driver, timeout=3).until\
                            (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "暂时没有任何商品")]')))
                        print(f'卖家无商品时，当前界面toast信息正常')
                    except:
                        print(f'卖家无商品时，前端界面展示存在问题')
                else:
                    if int(ProductReq.json()['total']) > 4:
                        RecelNum = 4
                    else:
                        RecelNum = int(ProductReq.json()['total'])
                    NameList = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_name")]')  # 商品名字
                    SalePriceList = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_money")]')   # 卖价
                    for i in range(RecelNum):
                        assert NameList[i].text == ProductReq.json()['rows'][i]['name']
                        if ProductReq.json()['rows'][i]['reShow'] == True:
                            assert SalePriceList[i].text == '已被恭请'
                        else:
                            if ProductReq.json()['rows'][i]['waitPrice'] == True:
                                assert SalePriceList[i].text == '估价待询'
                            else:
                                if 'salesPrice' in list(ProductReq.json()['rows'][i].keys()):
                                    assert float(str(SalePriceList[i].text).strip('¥').strip()) == \
                                           ProductReq.json()['rows'][i]['salesPrice']
                                    BeforeMoney = driver.find_element_by_xpath\
                                        (f'//*[contains(@resource-id, "recyclerView")]/android.widget.LinearLayout[{i}]/'
                                         f'android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]')
                                    assert float(str(BeforeMoney.text).strip('¥').strip()) == \
                                           float(ProductReq.json()['rows'][i]['originalPrice'])
                                else:
                                    assert float(str(SalePriceList[i].text).strip('¥').strip()) == \
                                           ProductReq.json()['rows'][i]['originalPrice']
            else:
                print(f'当前卖家无龖商城*店铺权限，跳过case')
        except:
            print(f'查看当前商家中心-龖商城商品存在问题，请测试人员及时查看')

    # 秒啪拍场列表展示
    def DelayAuction(self, driver, sellerId):
        if v5().getSellerCalcInfo_400(sellerId).json()['hasShop'] == True:
            TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
            TitleList[1].click()
        else:
            TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
            TitleList[0].click()
        try:
            DelayReq = v5().findDelayAucAuctionPage_420(sellerId)
            Total = int(DelayReq.json()['total'])
            if Total == 0:
                WebDriverWait(driver, timeout=3).until\
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "暂时没有任何拍场")]')))
                print(f'当前用户无秒啪拍场是前端界面toast信息正常')
            else:
                cmd(driver).small_up_swipe()
                # auction中心板块
                home_delayed_root = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_delayed_root")]')
                # 拍场名字
                DelayNameList = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_delayed_tv_name")]')
                # 拍场结束时间
                EndTimeList = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_delayed_tv_time")]')
                # 围观次数
                OBNumList = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_delayed_tv_count")]')
                # 拍品件数
                LotNumList = driver.find_elements_by_id( "home_delayed_tv_num")
                # 出价次数
                PriceNumList = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_delayed_tv_price_num")]')
                for i in range(1):
                    Name = DelayReq.json()['rows'][i]['name']
                    assert DelayNameList[i].text == Name    # 拍场名字验证
                    observerCount = DelayReq.json()['rows'][i]['observerCount']
                    assert ''.join(re.findall('\d', str(OBNumList[i].text))) == observerCount  # 围观次数
                    LotNum = DelayReq.json()['rows'][i]['lotCount']
                    assert ''.join(re.findall('\d', str(LotNumList[i].text))) == LotNum
                    biddingPriceCount = DelayReq.json()['rows'][i]['biddingPriceCount']
                    assert ''.join(re.findall('\d', str(PriceNumList[i].text))) == biddingPriceCount
                    if DelayReq.json()['rows'][i]['auctionState'] == 'F':
                        Status = '拍场已结束'
                        assert home_delayed_root[i].find_element_by_id('home_delayed_tv_time').text == Status
                        # 总成交额
                        TotalPrice = home_delayed_root[i].find_element_by_id('home_delayed_tv_price_fail').text
                        assert float(str(TotalPrice).strip('¥').strip()) == \
                               float(DelayReq.json()['rows'][i]['hammerPriceTotal'])
                    else:
                        assert "距结束" in home_delayed_root[i].find_element_by_id('home_delayed_tv_time').text
                        assert home_delayed_root[i].find_element_by_id('home_delayed_tv_state').text == '拍卖中'
        except:
            assert True == False

    # 轰啪商品列表展示
    def Auction(self, driver, sellerId):
        if v5().getSellerCalcInfo_400(sellerId).json()['hasShop'] == True:
            TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
            TitleList[2].click()
        else:
            TitleList = driver.find_elements_by_xpath("//*[contains(@resource-id, 'tv_tab_title')]")
            TitleList[1].click()
        time.sleep(1)
        try:
            Auction = v5().findApprovedAuctionByPage_230(sellerId)
            Total = int(Auction.json()['total'])
            if Total == 0:
                WebDriverWait(driver, timeout=3).until \
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "暂时没有任何拍场")]')))
                print(f'当前用户无秒啪拍场是前端界面toast信息正常')
            else:
                # cmd(driver).small_up_swipe()
                # 拍场名字
                AuctionNameList = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_name")]')
                AuctinonKeyWord = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_keyword")]')
                AuctionStatus = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_auc_auction_state")]')
                AuctionLotNum = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_lots")]')
                AuctionLotOB = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_observers")]')
                AuctionLotBidPrice = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_bidding_prices")]')
                for i in range(1):
                    assert AuctionNameList[i].text == Auction.json()['rows'][i]['name']
                    assert AuctinonKeyWord[i].text == Auction.json()['rows'][i]['keyword']
                    if Auction.json()['rows'][i]['auctionState'] == 'A':
                        AuctionText = '竞拍中'
                    elif Auction.json()['rows'][i]['auctionState'] == 'S':
                        AuctionText = '暂停中'
                    elif Auction.json()['rows'][i]['auctionState'] == 'F':
                        AuctionText = '已结束'
                    else:
                        AuctionText = '未开拍'
                    assert AuctionStatus[i].text == AuctionText
                    assert ''.join(re.findall('\d', AuctionLotNum[i].text)) == Auction.json()['rows'][i]['lots']
                    assert ''.join(re.findall('\d', AuctionLotOB[i].text)) == Auction.json()['rows'][i]['observers']
                    assert ''.join(re.findall('\d', AuctionLotBidPrice[i].text)) == Auction.json()['rows'][i]['biddingPrices']
        except:
            assert True == False