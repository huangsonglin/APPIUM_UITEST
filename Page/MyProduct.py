#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/18 9:46'

'''
我的宝贝界面
'''

import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import random,re
import time
from API.new_500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from API.V5down import *
import math
from Page.PulicClass import *
from Page.AddLot import *

class MyProduct:

    def check_page_init(self, driver):
        try:
            assert driver.current_activity == '.shop.goods.ui.GoodsListActivity'    # 首先判断当前界面的activity是否和预期一致
            assert driver.find_element_by_id('tv_title').text == '我的宝贝'
            classfylist = driver.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')
            assert len(classfylist) == 3
            # 添加轰啪拍品
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/tv_bid")))
            req = v5().hasDelayAucPermit_420()
            assert req.status_code == 200
            DelayAuction = req.json()['result']
            if DelayAuction:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/tv_delay")))
                except:
                    print(f'用户有秒啪权限时，添加秒啪宝贝按钮不可见')
        except Exception as e:
            raise e

    # 筛选类型
    def select(self, driver, Bidmodel=None):
        try:
            req = v5().getMemberPrivileges_500()
            assert req.status_code == 200
            DelayAuction = req.json()['putDelayAuction']
            Mallshop = req.json()['hasMallShop']
            SelectButton = driver.find_element_by_id('tv_search')
            SelectButton.click()
            driver.implicitly_wait(1)
            AllButton = WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.ID, 'tv_all')))
            AuctionButton = WebDriverWait(driver, timeout=10).until\
                (EC.visibility_of_element_located((By.ID, 'tv_auction')))
            if Bidmodel == None or Bidmodel == 'All':
                AllButton.click()
                time.sleep(1)
            elif Bidmodel == 'Auction':
                AuctionButton.click()
                time.sleep(1)
            elif Bidmodel == 'Shop':
                if Mallshop:
                    ShopButton = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.ID, 'tv_shop')))
                    ShopButton.click()
                else:
                    print(f'当前用户无店铺权限')
            elif Bidmodel == 'Delay':
                if DelayAuction:
                    DelayButton = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.ID, 'tv_delay')))
                    DelayAuction.click()
                else:
                    print(f'当前用户无秒啪权限')
            else:
                print(f'筛选类型错误，类型只能为:[All、Auction、Shop、Delay]')
        except Exception as e:
            raise e

    # 查看未上架的商品
    def check_unshelf_product(self, driver, Bidmodel=None):
        req = v5().findMyHoldProductPage_500(Bidmodel)
        # assert req.status_code == 200
        dreq = Down_V5Api().findMyHoldProductPage_420()
        NUM = dreq.json()['total']
        Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/btn_back')
        TitleList = driver.find_element_by_id('cn.dcpai.auction:id/tl_goods_type')
        TitleList.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[0].click()
        BOX = PulicClass().get_box(driver, TitleList)
        try:
            if int(NUM) == 0:
                print(f'当前用户未上架的商品，跳过这条case')
            else:
                productRootList = driver.find_elements_by_xpath\
                    ('//*[@resource-id="cn.dcpai.auction:id/recyclerView"]/android.widget.FrameLayout')
                if int(NUM) > 20:
                    RN = 15
                else:
                    RN = int(NUM)
                for i in range(RN):
                    # 名字
                    Name = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_name')
                    assert Name.text in dreq.json()['rows'][i]['name']
                    # 起拍价
                    StartPrice = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_begin_price')
                    assert float(''.join(re.findall('\d', StartPrice.text.replace(',', '')))) == \
                           float(dreq.json()['rows'][i]['beginPrice'])
                    # 市场估价
                    MaketPrice = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
                    assert dreq.json()['rows'][i]['marketPriceValue'] in MaketPrice.text
                    # 时间及结束
                    Time_Reason = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_observers')
                    assert Time_Reason.text == dreq.json()['rows'][i]['remark']
                    # 商品类型
                    ProductClassfy = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_auc_auction_state')
                    driver.drag_and_drop(Time_Reason, TitleList)
        except:
            print(f'查看当前用户未上架的商品，前端展示存在问题~~~')
            pass

    # 查看已上架商品
    def check_onself_product(self, driver, Bidmodel=None):
        req = v5().findMyInAucProductPage_500(Bidmodel)
        # assert req.status_code == 200
        dreq = Down_V5Api().findMyInAucProductPage_420()
        NUM = dreq.json()['total']
        Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/btn_back')
        TitleList = driver.find_element_by_id('cn.dcpai.auction:id/tl_goods_type')
        TitleList.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[1].click()
        BOX = PulicClass().get_box(driver, TitleList)
        try:
            if int(NUM) == 0:
                print(f'当前用户未上架的商品，跳过这条case')
            else:
                productRootList = driver.find_elements_by_xpath \
                    ('//*[@resource-id="cn.dcpai.auction:id/recyclerView"]/android.widget.FrameLayout')
                if int(NUM) > 20:
                    RN = 15
                else:
                    RN = int(NUM)
                for i in range(RN):
                    # 名字
                    Name = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_name')
                    assert Name.text in dreq.json()['rows'][i]['name']
                    # 当前价
                    MaketPrice = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
                    assert float(''.join(re.findall('\d', MaketPrice.text.replace(',', '')))) ==\
                           float(dreq.json()['rows'][i]['lotCurrentPrice'])
                    # 市场估价
                    Time_Reason = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_observers')
                    assert dreq.json()['rows'][i]['marketPriceValue'] in Time_Reason.text
                    # 商品类型
                    ProductClassfy = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_auc_auction_state')
                    driver.drag_and_drop(Time_Reason, TitleList)
        except:
            print(f'查看当前用户已上架的商品，前端展示存在问题~~~')
            pass

    # 查看已成交的商品
    def check_soldout_product(self, driver, Bidmodel=None):
        req = v5().findMySoldOutProductPage_500(Bidmodel)
        # assert req.status_code == 200
        dreq = Down_V5Api().findMySoldOutProductPage_420()
        NUM = dreq.json()['total']
        Back_Button = driver.find_element_by_id('cn.dcpai.auction:id/btn_back')
        TitleList = driver.find_element_by_id('cn.dcpai.auction:id/tl_goods_type')
        TitleList.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[1].click()
        BOX = PulicClass().get_box(driver, TitleList)
        try:
            if int(NUM) == 0:
                print(f'当前用户未上架的商品，跳过这条case')
            else:
                productRootList = driver.find_elements_by_xpath \
                    ('//*[@resource-id="cn.dcpai.auction:id/recyclerView"]/android.widget.FrameLayout')
                if int(NUM) > 20:
                    RN = 15
                else:
                    RN = int(NUM)
                for i in range(RN):
                    # 名字
                    Name = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_name')
                    assert Name.text in dreq.json()['rows'][i]['name']
                    # 起拍价
                    StartPrice = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_begin_price')
                    assert float(''.join(re.findall('\d', StartPrice.text.replace(',', '')))) == \
                           float(dreq.json()['rows'][i]['beginPrice'])
                    # 市场估价
                    MaketPrice = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
                    assert dreq.json()['rows'][i]['marketPriceValue'] in MaketPrice.text
                    # 时间及结束
                    Time_Reason = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_observers')
                    assert Time_Reason.text == dreq.json()['rows'][i]['remark']
                    # 商品类型
                    ProductClassfy = productRootList[0].find_element_by_id('cn.dcpai.auction:id/tv_auc_auction_state')
                    driver.drag_and_drop(Time_Reason, TitleList)
        except:
            print(f'查看当前用户已上架的商品，前端展示存在问题~~~')
            pass

    # 添加轰啪商品
    def check_add_auctionLot(self, driver):
        try:
            TitleList = driver.find_element_by_id('cn.dcpai.auction:id/tl_goods_type')
            TitleList.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[0].click()
            AddButton = WebDriverWait(driver, 2).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/tv_bid")))
            AddButton.click()
            driver.implicitly_wait(5)
            AddLot().add_auctionLot(driver)
        except:
            print(f'添加商品功能正常问题，请测试人员及时手动检查')
            assert True == False

    # 添加秒啪商品(未root真机无法运行)
    def check_add_delayacutionLot(self, driver):
        try:
            TitleList = driver.find_element_by_id('cn.dcpai.auction:id/tl_goods_type')
            TitleList.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[0].click()
            # 添加秒拍商品按钮
            AddButton = WebDriverWait(driver, 2).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/tv_delay")))
            AddButton.click()
            driver.back()
            AddButton.click()
            AddLot().add_delayAuctionLot(driver)
        except:
            print(f'添加商品功能正常问题，请测试人员及时手动检查')
            driver.back()
            pass










