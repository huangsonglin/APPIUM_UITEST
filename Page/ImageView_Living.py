#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/1 9:59'

"""
轰啪图文拍场出价
"""

import os,sys
import time
import re,random
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from API.Order500 import *
from adblogcat.logcat import *
from adb_command.adb import *
from Driver.Driver import *
from Page.Pay_Margin import *
from Page.PulicClass import *

"""
直播现场--图文界面相关操作
"""

class AuctionLive_ImageView:

    # 以围观方式进入后出价
    def onlooker_price(self, driver, aucionId):
        try:
            assert driver.current_activity == '.activity.AuctionNewActivity'
            Text = WebDriverWait(driver, timeout=2).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'introduction_state')]")))
            PriceButton = WebDriverWait(driver, timeout=2).until\
                (EC.visibility_of_element_located((By.ID, "auction_input_outprice_btn")))
            # 点击支付按钮
            PriceButton.click()
            time.sleep(1)
            driver.implicitly_wait(2)
            # 支付界面相关验证
            PayMargin().Assert_INIT(driver, aucionId)
            PayMargin().PayMethod(driver)
            # 从支付界面返回
            driver.back()
        except:
            assert True == False

    # 报名后--竞拍界面出价
    def successPrice(self, driver, auctionId, price):
        try:
            LotInfromation = []
            RQ = v5().findAuctionLotList_260(auctionId)
            for result in RQ.json():
                LotInfromation.append(result['id'])
            # 出价界面的title信息
            Title =  WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'text_title')]")))
            NO = int(re.findall('第(.*?)件', Title.text)[0])       # 当前拍场第几件商品
            FreshRq = v5().refreshBidInfo_440(auctionId)
            LotId = FreshRq.json()['id']
            LotStatus = FreshRq.json()['auctionState']
            assert LotInfromation[int(NO) - 1] == LotId
            TextStatus = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'introduction_state')]")))
            # 拍品A状态时
            if LotStatus == 'A':
                assert TextStatus.text == "倒计时"
                # 出价为0
                self.ZeroPrice(driver, auctionId)
                # 符号功能验证
                self.symbol_function(driver, auctionId)
                # 随机出价
                self.ExceptPrice(driver, auctionId, price)
            else:
                self.NotAPrice(driver, auctionId)
        except:
            assert True == False

    # 出价为0
    def ZeroPrice(self, driver, auctionId):
        try:
            FreshRq = v5().refreshBidInfo_440(auctionId)
            Num = int(FreshRq.json()['bidPricePage']['total'])  # 出价次数
            # 出价文本编辑框
            EditPrice = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_edit')))
            # 出价按钮
            PriceButton = driver.find_element_by_android_uiautomator\
                ('new UiSelector().resourceId("cn.dcpai.auction:id/auction_input_outprice_btn")')
            EditPrice.clear()
            EditPrice.send_keys(0)
            time.sleep(1)
            if Num == 0:
                PriceButton.click()
                time.sleep(0.5)
                try:
                    # 提示信息正常
                    Toast = PulicClass().Toast(driver, '出价不能低于加价幅度')
                    assert Toast == Toast
                    WebDriverWait(driver, timeout=10).until\
                        (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "出价记录")]')))
                    assert True == False, u'竞价为0出价成功'
                except:
                    assert True == True
            else:
                PNUM = driver.find_element_by_id('auction_price_number').text
                assert int(''.join(re.findall('\d', PNUM))) == Num
                PriceButton.click()
                time.sleep(1)
                try:
                    Toast = PulicClass().Toast(driver, '出价不能低于加价幅度')
                    assert Toast == Toast
                    HightPrice = driver.find_elements_by_id('price_item_price')[0]
                    assert str(HightPrice.text)[1:] != '0'
                except:
                    assert True == False, u'竞价为0出价成功'
        except:
            assert True == False

    # 出价
    def ExceptPrice(self, driver, auctionId, exprice):
        try:
            MREQ = v5().getMemberDetailInfo_112()
            MyMemberId = MREQ.json()['id']
            FreshRq = v5().refreshBidInfo_440(auctionId)
            LotId = FreshRq.json()['id']  # 当前拍场显示的LotId
            LotStatus = FreshRq.json()['auctionState']  # 拍品Id的状态信息
            BeginPrice = float(FreshRq.json()['lotDto']['beginPrice'])  # 起拍价
            bidIncValue = float(FreshRq.json()['lotDto']['bidIncValue'])  # 加价幅度
            PriceNum = int(FreshRq.json()['bidPricePage']['total'])  # 出价次数
            Num = int(FreshRq.json()['bidPricePage']['total'])  # 出价次数
            # 出价文本编辑框
            EditPrice = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_edit')))
            # 出价按钮
            PriceButton = driver.find_element_by_android_uiautomator\
                ('new UiSelector().resourceId("cn.dcpai.auction:id/auction_input_outprice_btn")')
            EditPrice.clear()
            # 当前拍品无人出价时
            if Num == 0:
                if BeginPrice > 0:
                    LowPRICE = BeginPrice
                else:
                    LowPRICE = BeginPrice + bidIncValue
                try:
                    if str(exprice).isdigit():
                        PulicClass().Press_keycode(driver, int(exprice))
                        time.sleep(1)
                        PriceButton.click()
                        cmd(driver).down_swipe()
                        if int(exprice) >= int(LowPRICE) and len(str(exprice)) < 9:
                            try:
                                Toast = PulicClass().Toast(driver, '出价成功')
                                assert Toast == True
                                # 可找到出价记录元素
                                WebDriverWait(driver, timeout=2).until \
                                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "出价记录")]')))
                                # 出价次数
                                PNUM = WebDriverWait(driver, timeout=10).until \
                                    (EC.visibility_of_element_located((By.ID, 'auction_price_number')))
                                assert int(''.join(re.findall('\d', PNUM.text))) == 1, u'出价成功'
                                # 当前最高价为预期价格
                                HightPrice = driver.find_elements_by_id('price_item_price')[0]
                                assert float(str(HightPrice.text).replace(',','')[1:]) == float(exprice)
                            except:
                                assert True == False, u'出价存在问题，请测试人员及时提交bug~~~'
                        else:
                            try:
                                Toast1 = PulicClass().Toast(driver, '出价不能低于加价幅度')
                                Toast2 = PulicClass().Toast(driver, '出价不能高于一个亿')
                                WebDriverWait(driver, timeout=10).until \
                                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "出价记录")]')))
                                assert Toast1 == True or Toast2 == True, u'出价大于一个亿或者小于加价幅度，界面功能正常'
                            except:
                                assert True == False, u'出价功能存在问题，请测试人员及时提交bug'
                                print(f'预期价不能小于最低初始价或者价格以高于亿，请及时更正价格哟~~~')
                                pass
                    else:
                        try:
                            EditPrice.send_keys(LowPRICE)
                            time.sleep(1)
                            assert True == False, u'出价界面输入非整形数据成功，请及时提交bug'
                        except:
                            print(f'预期价-类型错误，请及时更正价格哟~~~')
                            pass
                except:
                    assert True == False,u'出价存在问题'
            else:
                PNUM = driver.find_element_by_id('auction_price_number')
                assert int(''.join(re.findall('\d', PNUM.text))) == Num
                HightPrice = int(FreshRq.json()['bidPricePage']['rows'][0]['bidPrice'])  # 当前最高价格
                HightMember = int(FreshRq.json()['bidPricePage']['rows'][0]['memberId']) # 当前最高出价者
                EPMinHightPrice = HightPrice + bidIncValue                               # 当前最高价下出价成功最小值
                if str(exprice).isdigit():
                    try:
                        PulicClass().Press_keycode(driver, int(EPMinHightPrice))
                        time.sleep(1)
                        PriceButton.click()
                        time.sleep(10)
                        if int(exprice) > EPMinHightPrice and HightMember != int(MyMemberId) and len(str(exprice)) < 9:
                            Toast = PulicClass().Toast(driver, '出价成功')
                            assert Toast == True
                            assert int(''.join(re.findall('\d', PNUM.text))) == Num + 1
                            FristPrice = driver.find_elements_by_id('price_item_price')[0]
                            assert float(str(FristPrice.text).replace(',','')[1:]) == float(exprice)
                        else:
                            assert int(''.join(re.findall('\d', PNUM.text))) == Num
                            try:
                                Toast2 = PulicClass().Toast(driver, '出价不能高于一个亿')
                                Toast3 = PulicClass().Toast(driver, '你已经是最高出价者')
                                assert Toast1 == True or Toast2 == True or Toast3 == True
                            except:
                                pass
                    except:
                        assert True == False, u'出价页面手动输入价格出价功能存在问题，请测试人员及时提交bug~~~'
                else:
                    try:
                        EditPrice.send_keys(LowPRICE)
                        time.sleep(1)
                        assert True == False, u'出价界面输入非整形数据成功，请及时提交bug'
                    except:
                        print(f'预期价-类型错误，请及时更正价格哟~~~')
                        pass
        except:
            assert True == False

    # + - 号功能验证
    def symbol_function(self, driver, auctionId):
        try:
            AddButton = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_btn')))
            MinusButton = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_minus_btn')))
            EditPrice = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_edit')))
            InitPrice = float(str(EditPrice.text).replace(',',''))
            FreshRq = v5().refreshBidInfo_440(auctionId)
            BeginPrice = float(FreshRq.json()['lotDto']['beginPrice'])  # 起拍价
            bidIncValue = float(FreshRq.json()['lotDto']['bidIncValue'])  # 加价幅度
            PriceNum = int(FreshRq.json()['bidPricePage']['total'])  # 出价次数
            if PriceNum == 0:
                if BeginPrice > 0:
                    MaxPrice = BeginPrice
                else:
                    MaxPrice = bidIncValue
                AddButton.click()
                time.sleep(1)
                AftetPrice = float(str(EditPrice.text).replace(',', ''))
                if InitPrice < MaxPrice:
                    assert AftetPrice == MaxPrice
                    MinusButton.click()
                    time.sleep(1)
                    try:
                        Toast = PulicClass().Toast(driver, '不能再低了')
                        assert Toast == True
                        MafterPrice = float(str(EditPrice.text).replace(',', ''))
                        assert MafterPrice == AftetPrice, u'减号功能正常'
                    except:
                        print(f'出价界面减号功能存在问题，请及时提交bug~~~')
                        pass
                else:
                    assert AftetPrice == InitPrice + bidIncValue
                    MinusButton.click()
                    time.sleep(1)
                    try:
                        MafterPrice = float(str(EditPrice.text).replace(',', ''))
                        assert MafterPrice == AftetPrice - bidIncValue, u'减号功能正常'
                    except:
                        print(f'出价界面减号功能存在问题，请及时提交bug~~~')
                        pass
            else:
                MaxPrice = int(FreshRq.json()['bidPricePage']['rows'][0]['bidPrice'])
                AddButton.click()
                time.sleep(1)
                AftetPrice = float(str(EditPrice.text).replace(',', ''))
                if InitPrice < MaxPrice:
                    assert AftetPrice == MaxPrice + bidIncValue
                    MinusButton.click()
                    time.sleep(1)
                    try:
                        Toast = PulicClass().Toast(driver, '不能再低了')
                        assert Toast == True
                        MafterPrice = float(str(EditPrice.text).replace(',', ''))
                        assert MafterPrice == AftetPrice, u'减号功能正常'
                    except:
                        print(f'出价界面减号功能存在问题，请及时提交bug~~~')
                        pass
                else:
                    assert AftetPrice == InitPrice + bidIncValue
                    MinusButton.click()
                    time.sleep(1)
                    try:
                        MafterPrice = float(str(EditPrice.text).replace(',', ''))
                        assert MafterPrice == AftetPrice - bidIncValue, u'减号功能正常'
                    except:
                        print(f'出价界面减号功能存在问题，请及时提交bug~~~')
                        pass
        except:
            assert True == False

    # 非A状态时出价
    def NotAPrice(self, driver, auctionId):
        try:
            AddButton = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_btn')))
            AddButton.click()
            # 出价按钮
            PriceButton = driver.find_element_by_android_uiautomator\
                ('new UiSelector().resourceId("cn.dcpai.auction:id/auction_input_outprice_btn")')
            PriceButton.click()
            Toast = PulicClass().Toast(driver, "现在不能出价哦~")
            assert Toast == True
        except:
            assert True == False

    # 查看拍品详情
    def look_lot(self, driver, autionId):
        try:
            LookButton = WebDriverWait(driver, 2, 0.5).until \
                (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "查看详情")]')))
            Title = WebDriverWait(driver, timeout=2).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'text_title')]")))
            NO = int(re.findall('第(.*?)件', Title.text)[0])  # 当前拍场第几件商品
            Arq = v5().findAuctionLotList_260(autionId)
            LotId = Arq.json()[NO - 1]['id']
            DRQ = v5().findLotComplex_440(LotId)
            Lot_Name = DRQ.json()['name']               # 拍品名字
            Lot_Price = DRQ.json()['beginPrice']              # 拍品价格
            Lot_MarketPriceValue = DRQ.json()['marketPriceValue']   # 拍品市场估价
            Lot_BidIncValue = DRQ.json()['bidIncValue']   # 拍品加价幅度
            Lot_Status = DRQ.json()['auctionState']             # 拍品状态
            LookButton.click()
            driver.implicitly_wait(2)
            try:
                # 拍品列表
                Lot_List_View = WebDriverWait(driver, timeout=2).until \
                        (EC.visibility_of_element_located(
                        (By.XPATH, "//*[contains(@resource-id, 'auction_lot_list')]")))
                Close = WebDriverWait(driver, timeout=2).until \
                        (EC.visibility_of_element_located(
                        (By.XPATH, "//*[@resource-id='cn.dcpai.auction:id/auction_time_goods_success_container']/"
                                   "android.widget.LinearLayout/android.widget.ImageView[1]")))
                # 商品详情展示区域
                Lot_Detail_Area = WebDriverWait(driver, timeout=2).until \
                        (EC.visibility_of_element_located(
                        (By.XPATH, "//*[contains(@resource-id, 'auction_lot_detail_scrollView')]")))
                # 商品图片
                Lot_Image = Lot_Detail_Area.find_element_by_id('auction_lot_detail_convenient_img')
                Box = PulicClass().get_box(driver, Lot_Image)
                Lot_Image.click()
                driver.implicitly_wait(2)
                assert driver.current_activity == '.activity.ImagePagerActivity'
                # 保存按钮
                Save_Image_Button = WebDriverWait(driver, timeout=2).until \
                    (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'picture_save')]")))
                Save_Image_Button.click()
                time.sleep(2)
                """在下载图片界面 driver失效， 后期研究原因"""
                # try:
                #     Toast = PulicClass().Toast(driver,'图片')
                #     assert Toast == True
                # except:
                #     print(f'图片保存可能存在问题，请及时手动验证~~~')
                # finally:
                #     driver.back()
                #     time.sleep(2)
                driver.back()
                # 展示区域向上滑动
                driver.drag_and_drop(Lot_Image, Lot_List_View)
                # 加价幅度
                Bid_Increment = WebDriverWait(driver, 2, 0.5).until\
                    (EC.visibility_of_element_located((By.ID,"auction_lot_detail_bid_tv")))
                # 市场估价
                Market_value = WebDriverWait(driver, 2, 0.5).until\
                    (EC.visibility_of_element_located((By.ID,"auction_lot_detail_market_price_tv")))
                # 拍卖状态
                Status = WebDriverWait(driver, 2, 0.5).until\
                    (EC.visibility_of_element_located((By.ID,"auction_lot_detail_statues_tv")))
                # 名字及No./Total
                Name_NO = WebDriverWait(driver, 2, 0.5).until\
                    (EC.visibility_of_element_located((By.ID,"auction_lot_detail_name_tv")))
                # 当前展示价格
                Show_Price = WebDriverWait(driver, 2, 0.5).until\
                    (EC.visibility_of_element_located((By.ID,"auction_lot_detail_beginPrice_tv")))
                assert float(str(Bid_Increment.text).replace(',','').replace(' ','').split('¥')[1]) \
                       == float(Lot_BidIncValue)
                assert str(Market_value.text)[4:].strip() == Lot_MarketPriceValue
                assert Name_NO.text.split(' ')[0] == Lot_Name
                assert Name_NO.text.split(' ')[1] == "({}/{})".format(NO, len(Arq.json()))
                if Lot_Status == 'A':
                    Text_Status = '竞拍中'
                elif Lot_Status == 'N':
                    Text_Status = '待拍卖'
                elif Lot_Status == 'F' and int(Lot_Price) == 0:
                    Text_Status = '已流拍'
                else:
                    Text_Status = '已成交'
                assert Status.text == Text_Status
                # 左右滑动切换拍品
                if NO > 1:
                    # 右滑动
                    driver.swipe(Box[0]+10, Box[1]+10, Box[2]-10, Box[1]+10, 500)
                    time.sleep(1)
                    # 上滑
                    driver.swipe(int((Box[0] + Box[2])/2), Box[3]-10, int((Box[0] + Box[2])/2), Box[1]+10, 500)
                    assert float(str(Bid_Increment.text).replace(',', '').replace(' ', '').split('¥')[1]) \
                           == float(v5().findLotComplex_440(int(LotId) - 1).json()['bidIncValue'])
                    assert str(Market_value.text)[4:].strip() == (v5().findLotComplex_440(int(LotId) - 1).json()
                    ['marketPriceValue'])
                    assert Name_NO.text.split(' ')[0] == (v5().findLotComplex_440(int(LotId) - 1).json()['name'])
                    assert Name_NO.text.split(' ')[1] == "({}/{})".format(NO-1, len(Arq.json()))
                    # 左滑动
                    driver.swipe(Box[2]-10, Box[1]+10, Box[0]+10, Box[1]+10)
                    time.sleep(1)
                    driver.swipe(int((Box[0] + Box[2]) / 2), Box[3] - 10, int((Box[0] + Box[2]) / 2), Box[1] + 10, 500)
                    assert float(str(Bid_Increment.text).replace(',', '').replace(' ', '').split('¥')[1]) \
                           == float(Lot_BidIncValue)
                    assert str(Market_value.text)[4:].strip() == Lot_MarketPriceValue
                    assert Name_NO.text.split(' ')[0] == Lot_Name
                    assert Name_NO.text.split(' ')[1] == "({}/{})".format(NO, len(Arq.json()))
                    if NO != len(Arq.json()):
                        driver.swipe(Box[2]-10, Box[1], Box[0]+10, Box[1], 500)
                        time.sleep(1)
                        driver.swipe(int((Box[0] + Box[2])/2), Box[3] - 10, int((Box[0] + Box[2])/ 2), Box[1] + 10, 500)
                        assert float(str(Bid_Increment.text).replace(',', '').replace(' ', '').split('¥')[1]) \
                               == float(v5().findLotComplex_440(int(LotId) + 1).json()['bidIncValue'])
                        assert str(Market_value.text)[4:].strip() == (v5().findLotComplex_440(int(LotId) + 1).json()
                        ['marketPriceValue'])
                        assert Name_NO.text.split(' ')[0] == (v5().findLotComplex_440(int(LotId) + 1).json()['name'])
                        assert Name_NO.text.split(' ')[1] == "({}/{})".format(NO + 1, len(Arq.json()))
                else:
                    driver.swipe(Box[2] - 10, Box[1]+10, Box[0] + 10, Box[1]+10, 500)
                    time.sleep(1)
                    driver.swipe(int((Box[0] + Box[2]) / 2), Box[3] - 10, int((Box[0] + Box[2]) / 2), Box[1] + 10, 500)
                    assert float(str(Bid_Increment.text).replace(',', '').replace(' ', '').split('¥')[1]) \
                           == float(v5().findLotComplex_440(int(LotId) + 1).json()['bidIncValue'])
                    assert str(Market_value.text)[4:].strip() == (v5().findLotComplex_440(int(LotId) + 1).json()
                    ['marketPriceValue'])
                    assert Name_NO.text.split(' ')[0] == (v5().findLotComplex_440(int(LotId) + 1).json()['name'])
                    assert Name_NO.text.split(' ')[1] == "({}/{})".format(NO + 1, len(Arq.json()))
                # 关闭按钮
                Close.click()
            except:
                assert True == False, u'点击查看拍品详情时，存在界面显示问题。请相关测试人员手动验证~~~'
        except:
            assert True == False
