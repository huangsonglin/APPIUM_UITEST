#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/21 16:03'

import os,sys
import time
import re, string
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command as cmd
from selenium.webdriver.common.by import By
from API.new_500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Page.PulicClass import *
from Until.DB import *
from Page.Pay_Margin import *

class Delay_Auction_Page:

    Day = datetime.datetime.now().strftime('%Y%m%d%H%M%S')


    # 进入秒啪拍场界面后初始信息验证
    def Check_Page_InitSatus(self, driver):
        try:
            # 秒啪拍场界面的activity验证
            assert driver.current_activity == '.auction.delayed.ui.DelayedAuctionInfoAcitivity'
            # 私信
            Massge = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_info_chat_btn")))
            # 加关注
            Focus = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_info_focus_btn")))
            # 商家中心
            ShopCenter = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_head_btn_shop")))
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
        except:
            print(f'秒啪拍场页面初始信息状态存在问题， 请及时查看')
            driver.save_screenshot(IMG_PATH + f'\秒啪拍场页面初始信息状态_%%s.png' %self.Day)
            assert True == False

    # 秒啪信息详情验证
    def Check_DelayAuction_Imfromation(self, driver, delayauctionId):
        try:
            Req = v5().findDelayAucAuctionDetail_420(delayauctionId)
            status = Req.json()['auctionState']
            assert Req.status_code == 200
            # page Title
            Delay_Title = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_title_txt')
            assert (Delay_Title.text).replace('...', '') in Req.json()['name']
            # 卖家昵称
            Seller = driver.find_element_by_id('cn.dcpai.auction:id/delayed_head_txt_nickname')
            assert (Seller.text).replace('...', '') in Req.json()['memberNickname']
            # 保证金
            Deposit_Cash = driver.find_element_by_id('cn.dcpai.auction:id/delayde_info_txt_bid_bond')
            assert float(''.join(re.findall('\d', Deposit_Cash.text.replace(',', '')))) == float(Req.json()['bidBondAmount'])
            # 佣金比列
            Cash_Percentum = driver.find_element_by_id('cn.dcpai.auction:id/delayde_info_txt_commission')
            assert (Cash_Percentum.text).split(':')[1].strip()[0:-1] == Req.json()['buyerCommissionPercent']
            # 分类
            ClassFy = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_txt_category')
            assert (ClassFy.text).split(':')[1].strip() == Req.json()['categoryValue']
            # 拍品数量
            LotNum = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_txt_lot_count')
            assert ''.join(re.findall('\d', LotNum.text)) == Req.json()['lotCount']
            # 围观次数
            ObNum = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_txt_observer')
            try:
                # 围观次数貌似走的缓存数据不一致
                assert ''.join(re.findall('\d', ObNum.text.replace(',', ''))) == Req.json()['observerCount']
            except:
                pass
            # 拍场描述
            Delay_Desc = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_txt_desc')
            assert Delay_Desc.text[0:-3] in Req.json()['desc']
            # 拍场相关时间
            Delay_Time = driver.find_element_by_id('cn.dcpai.auction:id/delayed_head_txt_time')
            if status == 'F':
                assert Delay_Time.text == '已结束'
            elif status == 'A':
                assert '拍场剩余时间' in Delay_Time.text
            elif status == 'P':
                assert '拍场开始时间' in Delay_Time.text
        except:
            print(f'秒啪拍场页面详情信息与接口返回数据不一致， 请及时查看')
            assert True == False

    # 商品默认排序展示
    def Check_DelayLot_DefulteSort(self, driver, delayauctionId):
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId)
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
            Defeat.click()  # 指定默认排序
            driver.drag_and_drop(Defeat, Back_Button)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            for i in range(NUM-2):
                LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                for k in range(2):
                    # 拍品名字
                    LotName = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                    assert (LotName.text)[0:-3] in DefatReq.json()['rows'][2*i + k]['name']
                    # 当前价格
                    Current_Price = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                    # 出价按钮
                    PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                    # 拍品流拍状态情况
                    Leave = DefatReq.json()['rows'][2*i + k]['leave']
                    if Leave:
                        assert Current_Price.text == '已流拍'
                        assert PriceButton.text == '已流拍'
                        assert PriceButton.is_enabled() == False
                    else:
                        if DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'P':
                            assert PriceButton.text == '未开拍'
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['beginPrice']
                        elif DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'F':
                            assert PriceButton.text == '已成交'
                            assert PriceButton.is_enabled() == False
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['hammerPrice']
                        else:
                            assert PriceButton.text == '出价'
                            assert PriceButton.is_enabled() == True
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['currentPrice']
                    # 出价次数
                    Price_Total = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                    assert ''.join(re.findall('\d', Price_Total.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2*i + k]['biddingPriceCount']
                    # 围观次数
                    Onlookers = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_observer_num')
                    assert ''.join(re.findall('\d', Onlookers.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2 * i + k]['observerCount']
                driver.drag_and_drop(LotRoot[-1], Back_Button)
                time.sleep(1)
            [cmd(driver).down_swipe() for m in range(NUM)]
        except:
            print(f'秒啪拍场拍品排序功能存在问题')
            assert True == False

    # 围观次数降序排列
    def Check_OBNum_DescSort(self, driver, delayauctionId):
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId, order="DESC", sort="observerCount")
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
            Defeat.click()  # 指定默认排序
            Ob_Sort_Button.click()
            driver.drag_and_drop(Defeat, Back_Button)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            for i in range(NUM-2):
                LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                for k in range(2):
                    # 拍品名字
                    LotName = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                    assert (LotName.text)[0:-3] in DefatReq.json()['rows'][2*i + k]['name']
                    # 当前价格
                    Current_Price = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                    # 出价按钮
                    PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                    # 拍品流拍状态情况
                    Leave = DefatReq.json()['rows'][2*i + k]['leave']
                    if Leave:
                        assert Current_Price.text == '已流拍'
                        assert PriceButton.text == '已流拍'
                        assert PriceButton.is_enabled() == False
                    else:
                        if DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'P':
                            assert PriceButton.text == '未开拍'
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['beginPrice']
                        elif DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'F':
                            assert PriceButton.text == '已成交'
                            assert PriceButton.is_enabled() == False
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['hammerPrice']
                        else:
                            assert PriceButton.text == '出价'
                            assert PriceButton.is_enabled() == True
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['currentPrice']
                    # 出价次数
                    Price_Total = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                    assert ''.join(re.findall('\d', Price_Total.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2*i + k]['biddingPriceCount']
                    # 围观次数
                    Onlookers = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_observer_num')
                    assert ''.join(re.findall('\d', Onlookers.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2 * i + k]['observerCount']
                driver.drag_and_drop(LotRoot[-1], Back_Button)
                time.sleep(1)
            [cmd(driver).down_swipe() for i in range(NUM)]
        except:
            print(f'秒啪拍场拍品按照围观次数降序排序功能存在问题')
            assert True == False

    # 围观次数升序排列
    def Check_OBNum_ASCSort(self, driver, delayauctionId):
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId, order="ASC", sort="observerCount")
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
            Defeat.click()  # 指定默认排序
            Ob_Sort_Button.click()
            time.sleep(1)
            Ob_Sort_Button.click()
            driver.drag_and_drop(Defeat, Back_Button)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            for i in range(NUM-2):
                LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                for k in range(2):
                    # 拍品名字
                    LotName = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                    assert (LotName.text)[0:-3] in DefatReq.json()['rows'][2*i + k]['name']
                    # 当前价格
                    Current_Price = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                    # 出价按钮
                    PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                    # 拍品流拍状态情况
                    Leave = DefatReq.json()['rows'][2*i + k]['leave']
                    if Leave:
                        assert Current_Price.text == '已流拍'
                        assert PriceButton.text == '已流拍'
                        assert PriceButton.is_enabled() == False
                    else:
                        if DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'P':
                            assert PriceButton.text == '未开拍'
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['beginPrice']
                        elif DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'F':
                            assert PriceButton.text == '已成交'
                            assert PriceButton.is_enabled() == False
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['hammerPrice']
                        else:
                            assert PriceButton.text == '出价'
                            assert PriceButton.is_enabled() == True
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['currentPrice']
                    # 出价次数
                    Price_Total = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                    assert ''.join(re.findall('\d', Price_Total.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2*i + k]['biddingPriceCount']
                    # 围观次数
                    Onlookers = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_observer_num')
                    assert ''.join(re.findall('\d', Onlookers.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2 * i + k]['observerCount']
                driver.drag_and_drop(LotRoot[-1], Back_Button)
            time.sleep(1)
            [cmd(driver).down_swipe() for i in range(NUM)]
        except:
            print(f'秒啪拍场拍品围观次数升序排序功能存在问题')
            assert True == False

    # 价格降序排列
    def Check_PriceNum_DESCSort(self, driver, delayauctionId):
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId, order="DESC", sort="priceSeq")
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
            Defeat.click()  # 指定默认排序
            Price_Sort_Button.click()
            driver.drag_and_drop(Defeat, Back_Button)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            for i in range(NUM-2):
                LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                for k in range(2):
                    # 拍品名字
                    LotName = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                    assert (LotName.text)[0:-3] in DefatReq.json()['rows'][2*i + k]['name']
                    # 当前价格
                    Current_Price = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                    # 出价按钮
                    PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                    # 拍品流拍状态情况
                    Leave = DefatReq.json()['rows'][2*i + k]['leave']
                    if Leave:
                        assert Current_Price.text == '已流拍'
                        assert PriceButton.text == '已流拍'
                        assert PriceButton.is_enabled() == False
                    else:
                        if DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'P':
                            assert PriceButton.text == '未开拍'
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['beginPrice']
                        elif DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'F':
                            assert PriceButton.text == '已成交'
                            assert PriceButton.is_enabled() == False
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['hammerPrice']
                        else:
                            assert PriceButton.text == '出价'
                            assert PriceButton.is_enabled() == True
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['currentPrice']
                    # 出价次数
                    Price_Total = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                    assert ''.join(re.findall('\d', Price_Total.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2*i + k]['biddingPriceCount']
                    # 围观次数
                    Onlookers = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_observer_num')
                    assert ''.join(re.findall('\d', Onlookers.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2 * i + k]['observerCount']
                driver.drag_and_drop(LotRoot[-1], Back_Button)
                time.sleep(1)
            [cmd(driver).down_swipe() for i in range(NUM)]
        except:
            print(f'秒啪拍场拍品--出价次数降序排列功能存在问题')
            assert True == False

    # 价格升序排列
    def Check_PriceNum_ASCSort(self, driver, delayauctionId):
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId, order="ASC", sort="priceSeq")
            # 默认按钮
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            # 围观次数
            Ob_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_gather_num")))
            # 价格排序按钮
            Price_Sort_Button = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_price")))
            Defeat.click()  # 指定默认排序
            Price_Sort_Button.click()
            time.sleep(1)
            Price_Sort_Button.click()
            driver.drag_and_drop(Defeat, Back_Button)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            for i in range(NUM-2):
                LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                for k in range(2):
                    # 拍品名字
                    LotName = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                    assert (LotName.text)[0:-3] in DefatReq.json()['rows'][2*i + k]['name']
                    # 当前价格
                    Current_Price = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                    # 出价按钮
                    PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                    # 拍品流拍状态情况
                    Leave = DefatReq.json()['rows'][2*i + k]['leave']
                    if Leave:
                        assert Current_Price.text == '已流拍'
                        assert PriceButton.text == '已流拍'
                        assert PriceButton.is_enabled() == False
                    else:
                        if DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'P':
                            assert PriceButton.text == '未开拍'
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['beginPrice']
                        elif DefatReq.json()['rows'][2 * i + k]['auctionState'] == 'F':
                            assert PriceButton.text == '已成交'
                            assert PriceButton.is_enabled() == False
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['hammerPrice']
                        else:
                            assert PriceButton.text == '出价'
                            assert PriceButton.is_enabled() == True
                            assert ''.join(re.findall('\d', Current_Price.text.replace(',', ''))) == \
                                   DefatReq.json()['rows'][2 * i + k]['currentPrice']
                    # 出价次数
                    Price_Total = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                    assert ''.join(re.findall('\d', Price_Total.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2*i + k]['biddingPriceCount']
                    # 围观次数
                    Onlookers = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_observer_num')
                    assert ''.join(re.findall('\d', Onlookers.text.replace(',', ''))) == \
                           DefatReq.json()['rows'][2 * i + k]['observerCount']
                driver.drag_and_drop(LotRoot[-1], Back_Button)
            time.sleep(1)
            [cmd(driver).down_swipe() for i in range(NUM)]
        except:
            print(f'秒啪拍场拍品--出价升序排列功能存在问题')
            assert True == False

    # 商品出价
    def Check_DelayLot_BiddPrice(self, driver, delayauctionId):
        Req = v5().findDelayAucAuctionDetail_420(delayauctionId)
        print(Req.text)
        auctionState = Req.json()['auctionState']
        DefatReq = v5().findDelayAucAuctionLotPage_420(delayauctionId)
        print(DefatReq.text)
        try:
            Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/delayed_info_back_btn')
            Defeat = WebDriverWait(driver, 3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/delayed_txt_default")))
            driver.drag_and_drop(Defeat, Back_Button)
            time.sleep(5)
            NUM = math.ceil(int(DefatReq.json()['total']) / 2)
            if NUM == 1:
                NUM == 1
            else:
                NUM = NUM -1
            if auctionState == 'F':
                for i in range(NUM):
                    LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                    for k in range(2):
                        # 出价按钮
                        PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                        assert PriceButton.text in ['已成交', '已流拍']
                        assert PriceButton.is_enabled() == False
            elif auctionState == 'P':
                for i in range(NUM):
                    LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                    for k in range(2):
                        # 出价按钮
                        PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                        assert PriceButton.text == '未开拍'
                        assert PriceButton.is_enabled() == False
            else:
                AutoApply = v5().autoDelayAucAuctionRegister_420(delayauctionId)
                for i in range(NUM):
                    LotRoot = driver.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                    for k in range(2):
                        lotstatus = DefatReq.json()['rows'][2*i + k]['auctionState']
                        # 出价按钮
                        PriceButton = LotRoot[k].find_element_by_id('cn.dcpai.auction:id/delayed_info_price')
                        if lotstatus == 'F':
                            assert PriceButton.text in ['已成交', '已流拍']
                            assert PriceButton.is_enabled() == False
                            print(f'当前拍品已结束, 跳过')
                        else:
                            PriceButton.click()
                            time.sleep(1)
                            if AutoApply.json()['registered'] == False:
                                PayMargin().DelayAuction_INIT(driver, delayauctionId)
                            else:
                                # 如果是第一次报名进入拍场
                                try:
                                    Toast = WebDriverWait(driver, timeout=5).until \
                                        (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text,"知道了")]')))
                                    Toast.click()
                                except:
                                    pass
                                try:
                                    # 编辑出价框
                                    EditPriceBox = WebDriverWait(driver, 3).until\
                                        (EC.visibility_of_element_located((By.ID, "et_bid_price")))
                                    # 当前领先价
                                    CurrentPrice = WebDriverWait(driver, 3).until\
                                        (EC.visibility_of_element_located((By.ID, "tv_bid_price")))
                                    if float(DefatReq.json()['rows'][2*i + k]['currentPrice']) == 0:
                                        assert float(''.join(re.findall('\d', EditPriceBox.text.replace(',', '')))) == \
                                               float(DefatReq.json()['rows'][2 * i + k]['beginPrice'])
                                    else:
                                        assert float(''.join(re.findall('\d', EditPriceBox.text.replace(',', '')))) == \
                                               float(DefatReq.json()['rows'][2 * i + k]['currentPrice']) + \
                                               float(DefatReq.json()['rows'][2 * i + k]['bidIncValue'])
                                    assert float(''.join(re.findall('\d', CurrentPrice.text.replace(',', '')))) == \
                                           float(DefatReq.json()['rows'][2*i + k]['currentPrice'])
                                    # 匿名登录
                                    AnonymityPrice = WebDriverWait(driver, 3).until\
                                        (EC.visibility_of_element_located((By.ID, 'swb_use_anonymity')))
                                    AnonymityPrice.get_attribute('checked')
                                    # 委托出价按钮
                                    EntrustedBid = WebDriverWait(driver, 3).until\
                                        (EC.visibility_of_element_located((By.ID, 'tv_entrust')))
                                    # 立即出价按钮
                                    NowBid = WebDriverWait(driver, 3).until \
                                        (EC.visibility_of_element_located((By.ID, 'tv_bid')))
                                    EntrustedBid.click()
                                    time.sleep(1)
                                    AlertTile = WebDriverWait(driver, 2).until\
                                        (EC.visibility_of_element_located(By.ID, 'android:id/message'))
                                    assert ''.join(re.findall('\d', AlertTile.text.replace(',', ''))) == \
                                           ''.join(re.findall('\d', EditPriceBox.text.replace(',', '')))
                                    driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
                                    assert PulicClass().Toast(driver, '当前价格必须大于或等于')
                                except:
                                    print(f'竞拍中的商品点击出价后未弹出对应的出价框, 请测试人员及时手动测试验证~~~~')
                                    pass
                    driver.drag_and_drop(LotRoot[-1], Back_Button)
        except:
            assert True == False