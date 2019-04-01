#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/11 9:53'

"""
龖*竞拍页面
"""

import os,sys
import time,math
import re,random
from Until.YamlRead import *
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from API.new_500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Page.PulicClass import *


class D_Auction_Page:
    # dr = Driver().get_driver()

    def Into_Page(self, dr):
        PulicClass().Into_Da_Auction(dr)
        dr.implicitly_wait(2)
        time.sleep(1)

    # 龖*竞拍-秒啪初始页面信息
    def DelayAuction_InitPage(self, dr):
        self.Into_Page(dr)
        try:
            SystemReq = v5().getSysDelayMsg_431()
            Get_Auction = v5().futureDelayAucAuctionPage_430()
            # 轰啪拍场按钮
            Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "轰啪拍场")]')
            # 秒啪拍场
            Delay_Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "秒啪拍场")]')
            Delay_Auction_Button.click()
            # 我的参拍
            My_compete = dr.find_element_by_id('mes_remind__tv')
            if SystemReq.json()['sysDelayMsgCount'] != '0':
                # 参拍的系统提示消息的数据统计
                show_sys_num = ''.join(re.findall('\d', dr.find_element_by_id('mes_remind_count_tv').text))
                assert show_sys_num == SystemReq.json()['sysDelayMsgCount']
                My_compete.click()
                time.sleep(1)
                dr.back()
                try:
                    dr.find_element_by_id('mes_remind_count_tv')
                    print(f'点击查看未读信息后，前端界面未读信息未及时清空~~~')
                    assert True == False
                except:
                    assert True == True
            # 拍场分类列表
            classfy_list = dr.find_element_by_id('sdf_scrollview')
            # 添加更多分类
            add_more_classfy = dr.find_element_by_id('sdf_add')
            # 分类下秒啪拍场的总数
            Num = int(Get_Auction.json()['total'])
            if Num == 0:
                Toast = PulicClass().Toast(dr, '暂时没有任何拍场')
                Refresh = PulicClass().Toast(dr, '点击重试')
                assert Toast == Refresh == True
            else:
                [cmd(dr).up_swipe() for i in range(Num)]
                # 点击查看历史拍场按钮
                histroy_auction = dr.find_element_by_android_uiautomator\
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/foot_txt_history")')
                [cmd(dr).down_swipe() for i in range(Num)]
        except:
            print(f'龖竞拍界面初始化状态显示存在一定的问题，请相关测试人员手动验证~~~~')
            assert True == False

    # 查看秒啪拍场--更多分类
    def Find_DelayAction_Add_Classfy(self, dr):
        self.Into_Page(dr)
        # 可见分类名字
        display_classfy = []
        try:
            # 秒啪拍场
            Delay_Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "秒啪拍场")]')
            Delay_Auction_Button.click()
            dr.implicitly_wait(2)
            # 拍场分类列表
            classfy_list = dr.find_element_by_id('sdf_scrollview')
            classfy_names = dr.find_elements_by_id('cn.dcpai.auction:id/title')
            for classfy_name in classfy_names:
                display_classfy.append(classfy_name.text)
            # 更多分类
            add_more_classfy = dr.find_element_by_id('sdf_add')
            add_more_classfy.click()
            time.sleep(2)
            try:
                # 添加分类界面
                page_display_classfy = []
                # 页面提示信息
                dr.find_element_by_android_uiautomator('new UiSelector().text("点击跳转对应分类")')
                page_classfy_names = dr.find_elements_by_id('cn.dcpai.auction:id/type_name')
                for page_classfy_name in page_classfy_names:
                    page_display_classfy.append(page_classfy_name.text)
                for name in display_classfy:
                    assert name in page_classfy_name
                # 随机点击一个分类
                page_classfy_names[random.randint(0, len(page_classfy_names)-1)].click()
                time.sleep(1)
            except:
                print(f'龖*竞拍点击跳转更多分类功能存在问题，请相关测试人员手动验证~~~~')
                assert True == False
        except:
            print(f'龖*竞拍-秒啪拍场--相关信息存在问题')
            assert True == False

    # 点击查看我的参拍
    def Find_DelayAction_My_Compete(self, dr):
        self.Into_Page(dr)
        MyReq = v5().findMyLotPartakePage_432()
        Total = int(MyReq.json()['total'])
        try:
            # 秒啪拍场
            Delay_Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "秒啪拍场")]')
            Delay_Auction_Button.click()
            dr.implicitly_wait(2)
            My_compete = dr.find_element_by_id('mes_remind__tv')
            My_compete.click()
            time.sleep(1)
            assert dr.current_activity == '.auction.delayed.ui.DelayedPriceListActivity'
            if Total == 0:
                try:
                    # 暂时没有任何拍品的文字提示信息
                    dr.find_element_by_android_uiautomator('new UiSelector().text("暂时没有任何拍品")')
                    Refresh_Button = dr.find_element_by_android_uiautomator('new UiSelector().text("点击重试")')
                    assert bool(Refresh_Button.get_attribute('clickable')) == True
                    Refresh_Toast = PulicClass().Toast(dr, '点击重试')
                    assert Refresh_Toast == True
                except:
                    print(f'当前无参拍信息时，我的参拍界面信息存在问题。请测试人员手动验证~~~~')
                    assert True == False
            else:
                # 拍品暂时区域
                Delay_Lot_Root = dr.find_elements_by_id('cn.dcpai.auction:id/delayed_root')
                # 围观次数
                Ob_Nums = dr.find_elements_by_id('delaye_item_txt_observer_num')
                # 当前拍品状态信息
                Lot_My_Status = dr.find_elements_by_id('cn.dcpai.auction:id/delayed_item_state')
                # 查看当前屏前端显示的信息
                for i in range(len(Delay_Lot_Root)):
                    try:
                        # 拍品名字
                        Delay_Lot_Name = Delay_Lot_Root[i].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_name')
                        assert Delay_Lot_Name.text == MyReq.json()['rows'][i]['name']
                        # 当前拍品--我的状态信息
                        Delay_Lot_Status = Delay_Lot_Root[i].find_element_by_id('delayed_item_state')
                        if MyReq.json()['rows'][i]['auctionState'] == 'A' and MyReq.json()['rows'][i]['currentBidder']:
                            Text_Status = '领先'
                        elif MyReq.json()['rows'][i]['auctionState'] == 'A' and not MyReq.json()['rows'][i]['currentBidder']:
                            Text_Status = '落后'
                        elif MyReq.json()['rows'][i]['auctionState'] == 'F' and MyReq.json()['rows'][i]['currentBidder']:
                            Text_Status = '中拍'
                        else:
                            Text_Status = '流拍'
                        assert Text_Status == Delay_Lot_Status.text
                        # 拍品当前价格
                        Delay_Lot_Price = Delay_Lot_Root[i].find_element_by_id('cn.dcpai.auction:id/delayed_item_txt_price')
                        assert float(''.join(re.findall('\d', (Delay_Lot_Price.text).replace(',', '')))) == \
                               float(MyReq.json()['rows'][i]['currentPrice'])
                        # 出价次数
                        Price_Num = Delay_Lot_Root[i].find_element_by_id('cn.dcpai.auction:id/delaye_item_txt_price_num')
                        assert ''.join(re.findall('\d', Price_Num.text)) == MyReq.json()['rows'][i]['biddingPriceCount']
                        # 围观次数
                        Ob_Num = Delay_Lot_Root[i].find_element_by_id('delaye_item_txt_observer_num')
                        assert ''.join(re.findall('\d', Ob_Num.text)) == MyReq.json()['rows'][i]['observerCount']
                        if i == 1:
                            PulicClass().swipe_random_up(dr, 60)
                    except:
                        print(f'我参与的拍品详细信息存在问题，请相关人员手动查看~~~')
            dr.back()
        except:
            assert True == False

    # 点击查看历史拍场
    def find_histroy_delayauction(self, dr):
        self.Into_Page(dr)
        HistroyReq = v5().historyDelayAucAuctionPage_420()
        NUM = int(HistroyReq.json()['total'])
        if NUM >= 4:
            M = 4
        else:
            M = NUM
        try:
            # 秒啪拍场
            Delay_Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "秒啪拍场")]')
            Delay_Auction_Button.click()
            loc = (By.XPATH, "//*[contains(@text, '查看历史拍场')]")
            PulicClass().up_swipe_to_display(dr, *loc)
            HistoryButton = WebDriverWait(dr, 2).until(EC.visibility_of_element_located(loc))
            HistoryButton.click()
            time.sleep(1)
            assert dr.current_activity == '.frame.da.ui.HistoryDelayedActivity', u'历史拍场界面activity正常'
            Page_Title = WebDriverWait(dr, 5).until\
                (EC.visibility_of_element_located((By.XPATH,"//*[@text='秒啪历史拍场']")))
            # 秒啪分类
            Classfy_List = dr.find_elements_by_id('cn.dcpai.auction:id/title')
            # 查看更多分类
            More_Classfy = dr.find_element_by_id('cn.dcpai.auction:id/sdf_add')
            # 点击全部查看
            Classfy_List[0].click()
            # 秒啪展示信息整个板块
            Display_Area = dr.find_elements_by_id('cn.dcpai.auction:id/home_delayed_root')
            OriginBox = PulicClass().get_box(dr, Display_Area[0])
            MaxNum = len(Display_Area)
            for i in range(M):
                # 拍品名字
                Delay_Auction_Name = Display_Area[0].find_element_by_id('cn.dcpai.auction:id/home_delayed_tv_name').text
                # 围观次数
                Delay_Auction_ObNum = ''.join(re.findall
                                              ('\d', (Display_Area[0].find_element_by_id
                                                      ('home_delayed_tv_count').text).replace(',', '')))
                # 拍品件数
                Delay_Auction_LotNum = ''.join(re.findall
                                               ('\d', Display_Area[0].find_element_by_id('home_delayed_tv_num').text))
                ELE = Display_Area[0].find_element_by_id('home_delayed_tv_price_num')
                # 出价次数
                Delay_Auction_PriceNum = ''.join(re.findall
                                               ('\d', ELE.text))
                # 成交总额
                Delay_Auction_TotalPrice = ''.join(re.findall
                                                   ('\d', (Display_Area[0].find_element_by_id
                                                           ('home_delayed_tv_price_fail').text).replace(',', '')))
                assert Delay_Auction_Name == HistroyReq.json()['rows'][i]['name']
                assert Delay_Auction_LotNum == HistroyReq.json()['rows'][i]['lotCount']
                assert Delay_Auction_PriceNum == HistroyReq.json()['rows'][i]['biddingPriceCount']
                assert float(Delay_Auction_TotalPrice) == float(HistroyReq.json()['rows'][i]['hammerPriceTotal'])
                assert Delay_Auction_ObNum == HistroyReq.json()['rows'][i]['observerCount']
                # 向上滑动一个展示框的位置
                PulicClass().touch_swipe(dr, ELE, OriginBox[0], OriginBox[1] - 35)
            dr.back()
        except:
            assert True == False

    # 查看全部列表中的前5个拍场信息
    def find_all_top5_auction(self, dr):
        self.Into_Page(dr)
        Areq = v5().futureDelayAucAuctionPage_430()
        NUM = int(Areq.json()['total'])
        try:
            # 秒啪拍场
            Delay_Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "秒啪拍场")]')
            Delay_Auction_Button.click()
            if NUM == 0:
                Toast = PulicClass().Toast(dr, '暂时没有任何拍场')
                Refresh = PulicClass().Toast(dr, '点击重试')
                assert Toast == Refresh == True
            else:
                if NUM >= 5:
                    M = 5
                else:
                    M = NUM
                    # 秒啪展示信息整个板块
                    Display_Area = dr.find_elements_by_id('cn.dcpai.auction:id/home_delayed_root')
                    OriginBox = PulicClass().get_box(dr, Display_Area[0])
                    MaxNum = len(Display_Area)
                    for i in range(M):
                        # 拍品名字
                        Delay_Auction_Name = Display_Area[0].find_element_by_id(
                            'cn.dcpai.auction:id/home_delayed_tv_name').text
                        # 围观次数
                        Delay_Auction_ObNum = ''.join(re.findall
                                                      ('\d', (Display_Area[0].find_element_by_id
                                                              ('home_delayed_tv_count').text).replace(',', '')))
                        # 拍品件数
                        Delay_Auction_LotNum = ''.join(re.findall
                                                       ('\d',
                                                        Display_Area[0].find_element_by_id('home_delayed_tv_num').text))
                        ELE = Display_Area[0].find_element_by_id('home_delayed_tv_price_num')
                        # 出价次数
                        Delay_Auction_PriceNum = ''.join(re.findall
                                                         ('\d', ELE.text))

                        assert Delay_Auction_Name == Areq.json()['rows'][i]['name']
                        assert Delay_Auction_LotNum == Areq.json()['rows'][i]['lotCount']
                        assert Delay_Auction_ObNum == Areq.json()['rows'][i]['observerCount']
                        assert Delay_Auction_PriceNum == Areq.json()['rows'][i]['biddingPriceCount']
                        # 向上滑动一个展示框的位置
                        PulicClass().touch_swipe(dr, ELE, OriginBox[0], OriginBox[1] - 35)
        except:
            assert True == False

    # 龖*竞拍-轰啪拍场初始页面信息
    def Auction_InitPage(self, dr):
        self.Into_Page(dr)
        time.sleep(2)
        try:
            # 轰啪拍场按钮
            Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "轰啪拍场")]')
            Auction_Button.click()
            dr.implicitly_wait(3)
            GetAuction = v5().futureAuctionList_270()
            assert GetAuction.status_code == 200
            Num = GetAuction.json()['total']
            if int(Num) == 0:
                Toast = PulicClass().Toast(dr, '暂时没有任何拍场')
                Refresh = PulicClass().Toast(dr, '点击重试')
                assert Toast == Refresh == True
            else:
                # 第一个拍场的名字
                FristName = dr.find_elements_by_id('cn.dcpai.auction:id/home_exquisite_tv_name')[0].text
                # 第一个拍场的围观次数
                FristObNum = dr.find_elements_by_id('cn.dcpai.auction:id/home_exquisite_tv_count')[0].text
                FristObNum = ''.join(re.findall('\d', FristObNum))
                assert FristName == GetAuction.json()['rows'][0]['name']
                assert FristObNum == GetAuction.json()['rows'][0]['observerCount']
                for i in range(int(Num)):
                    AuctionRoot = dr.find_elements_by_id('cn.dcpai.auction:id/home_exquisite_root')
                    name = AuctionRoot[0].find_element_by_id('home_exquisite_tv_name')
                    # 元素-拍场围观次数
                    obnum = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_count')
                    # 元素-据结束时间
                    startTime = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_time')
                    # 元素-拍场拍品图片列表
                    lotList = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_recycler')
                    assert name.text == GetAuction.json()['rows'][i]['name']
                    assert ''.join(re.findall('\d', str(obnum.text).replace(',', ''))) == \
                           GetAuction.json()['rows'][i]['observerCount']
                    dr.drag_and_drop(lotList, Auction_Button)
                    time.sleep(1)
                    Y = PulicClass().get_box(dr, obnum)[3] - PulicClass().get_box(dr, name)[1]
                    PulicClass().randow_hight_swipe(dr, Y)
                    time.sleep(1)
            # 历史拍场
            loc = (By.XPATH, '//*[contains(@resource-id, "cn.dcpai.auction:id/foot_txt_history")]')
            PulicClass().down_swipe_to_display(dr, *loc)
        except:
            assert True == False

    # 查看轰啪拍场历史信息
    def find_histroy_auction(self, dr):
        self.Into_Page(dr)
        GetHistroy = v5().historyAuctionList_270()
        assert GetHistroy.status_code == 200
        try:
            # 轰啪拍场按钮
            Auction_Button = dr.find_element_by_xpath('//*[contains(@text, "轰啪拍场")]')
            Auction_Button.click()
            dr.implicitly_wait(3)
            # 历史拍场
            loc = (By.XPATH, '//*[contains(@text, "查看历史拍场")]')
            PulicClass().down_swipe_to_display(dr, *loc)
            time.sleep(1)
            HistroyButton = WebDriverWait(dr, 5).until(EC.visibility_of_element_located(loc))
            PulicClass().touch_tap(dr, HistroyButton)
            dr.implicitly_wait(3)
            time.sleep(1)
            assert dr.current_activity == '.frame.da.ui.HistoryAuctionActivity'
            # 元素-页面title
            page_title = dr.find_element_by_android_uiautomator('new UiSelector().text("轰啪历史拍场")')
            if int(GetHistroy.json()['total']) > 5:
                NUM = 5
            else:
                NUM = int(GetHistroy.json()['total'])
            for i in range(NUM):
                AuctionRoot = dr.find_elements_by_id('cn.dcpai.auction:id/home_exquisite_root')
                name = AuctionRoot[0].find_element_by_id('home_exquisite_tv_name')
                # 元素-拍场围观次数
                obnum = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_count')
                # 元素-拍场结束时间
                startTime = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_time')
                # 元素-总成交额
                totalprice = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_price')
                # 元素-总出价次数
                totalpriceNum = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_tv_num')
                # 元素-拍场拍品图片列表
                lotList = AuctionRoot[0].find_element_by_id('cn.dcpai.auction:id/home_exquisite_recycler')
                assert name.text == GetHistroy.json()['rows'][i]['name']
                assert ''.join(re.findall('\d', str(obnum.text).replace(',', ''))) == \
                       GetHistroy.json()['rows'][i]['observerCount']
                RQStartTime = GetHistroy.json()['rows'][i]['startTime']
                if str(datetime.datetime.now().date()) in RQStartTime:
                    RQStartTime = '今天' + RQStartTime.split(str(datetime.datetime.now().date()))[1][0:-3]
                else:
                    RQStartTime = RQStartTime[5:-3]
                    RQStartTime = RQStartTime.replace('-', '月').split(' ')
                    RQStartTime = RQStartTime[0]+'日 '+ RQStartTime[1]
                assert  RQStartTime == startTime.text
                assert float(''.join(re.findall('\d', str(totalprice.text).replace(',', '')))) == \
                       float(GetHistroy.json()['rows'][i]['hammerPriceTotal'])
                assert ''.join(re.findall('\d', str(totalpriceNum.text).replace(',', ''))) == \
                       GetHistroy.json()['rows'][i]['biddingPriceCount']
                dr.drag_and_drop(lotList, page_title)
                time.sleep(1)
                Y = PulicClass().get_box(dr, obnum)[3] - PulicClass().get_box(dr, name)[1]
                PulicClass().randow_hight_swipe(dr, Y)
                time.sleep(1)
        except:
            assert True == False



if __name__ == '__main__':
    dr = Driver().get_driver()
    D_Auction_Page().Auction_InitPage(dr)




