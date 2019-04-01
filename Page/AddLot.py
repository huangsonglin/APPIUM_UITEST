#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/27 13:53'


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
from API.V5down import *
from Command.command import command as cmd


class AddLot:

    Day = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # 添加轰啪商品
    def add_auctionLot(self, driver):
        try:
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.AddBabyActivity', u'添加轰啪商品界面activity正常'
            # 页面title
            PageTitle = driver.find_element_by_id('cn.dcpai.auction:id/tv_title')
            assert PageTitle.text == '新增宝贝'
            # 确认添加商品
            SureButton = driver.find_element_by_id('cn.dcpai.auction:id/btn_right')
            # 添加图片按钮
            add_picture = driver.find_element_by_id('cn.dcpai.auction:id/ib_add_pic')
            add_picture.click()
            assert driver.current_activity == 'com.lzy.imagepicker.ui.ImageGridActivity', u'选择照片界面activity正常'
            CheckBoxList = driver.find_elements_by_id('cn.dcpai.auction:id/cb_check')
            for i in range(len(CheckBoxList) - 4):
                CheckBoxList[i].click()
            driver.find_element_by_id('cn.dcpai.auction:id/btn_ok').click()
            PulicClass().touch_tap(driver, SureButton)
            # 添加名字
            add_name = driver.find_element_by_id('cn.dcpai.auction:id/et_name')
            add_name.clear()
            add_name.send_keys(PulicClass().Chinese(5))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "拍卖时长不能为空") == True, u'添加照片和名字后点击完成，功能正常'
            except:
                driver.save_screenshot(IMG_PATH + r'\AddAuctionLot_%s.png' % self.Day)
                pass
            # 拍卖时长
            add_lot_time = driver.find_element_by_id('cn.dcpai.auction:id/tv_plan_time_key')
            add_lot_time.click()
            # 拖动改变时间
            TimeList = driver.find_elements_by_class_name('android.widget.TextView')  # 时间列表
            [driver.drag_and_drop(TimeList[-1], TimeList[int(len(TimeList) / 2)]) for i in range(2)]
            driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            time.sleep(1)
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "市场估价不能为空") == True, u'功能正常'
            except:
                driver.save_screenshot(IMG_PATH + r'\AddAuctionLot_%s.png' % self.Day)
                pass
            # 添加市场估价
            add_lot_markervalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
            add_lot_markervalue.click()
            TimeList = driver.find_elements_by_class_name('android.widget.TextView')  # 时间列表
            [driver.drag_and_drop(TimeList[-1], TimeList[int(len(TimeList) / 2)]) for i in range(2)]
            driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "藏品类别不能为空") == True, u'功能正常'
            except:
                driver.save_screenshot(IMG_PATH + r'\AddAuctionLot_%s.png' % self.Day)
                pass
            # 添加拍品类型
            add_lot_type = driver.find_element_by_id('cn.dcpai.auction:id/tv_type')
            add_lot_type.click()
            TimeList = driver.find_elements_by_class_name('android.widget.TextView')  # 时间列表
            [driver.drag_and_drop(TimeList[-1], TimeList[int(len(TimeList) / 2)]) for i in range(2)]
            driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "起拍价必填") == True, u'功能正常'
            except:
                driver.save_screenshot(IMG_PATH + r'\AddAuctionLot_%s.png' % self.Day)
                pass
            # 设置起拍价
            add_lot_beginprice = driver.find_element_by_id('cn.dcpai.auction:id/et_begin_price')
            add_lot_beginprice.clear()
            PulicClass().Press_keycode(driver, random.randint(0, 100))
            loc = (By.ID, "cn.dcpai.auction:id/tv_bid_inc_value")
            PulicClass().up_swipe_to_display(driver, *loc)
            # 加价幅度
            add_lot_bidvalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_bid_inc_value')
            add_lot_bidvalue.click()
            TimeList = driver.find_elements_by_class_name('android.widget.TextView')  # 时间列表
            [driver.drag_and_drop(TimeList[-1], TimeList[int(len(TimeList) / 2)]) for i in range(2)]
            driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            # 简介
            desc_loc = (By.ID, "cn.dcpai.auction:id/tv_desc")
            PulicClass().up_swipe_to_display(driver, *desc_loc)
            add_lot_desc = driver.find_element_by_id('cn.dcpai.auction:id/tv_desc')
            add_lot_desc.click()
            time.sleep(1)
            assert driver.current_activity == '.activity.ProductDescModifyActivity'
            EditBox = driver.find_element_by_id('cn.dcpai.auction:id/et_desc')
            EditBox.clear()
            EditBox.send_keys(PulicClass().Chinese(30))
            driver.find_element_by_id('cn.dcpai.auction:id/btn_back').click()
            SureButton.click()
            try:
                # assert PulicClass().Toast(driver, "添加成功")
                assert driver.current_activity == '.shop.goods.ui.GoodsListActivity'
                print(f'添加轰啪商品成功~~~')
            except:
                driver.save_screenshot(IMG_PATH + r'\AddAuctionLot_%s.png' % self.Day)
                pass
        except:
            print(f'添加轰啪商品失败，请测试人员及时手动查看~~~')

    # 添加秒啪商品
    def add_delayAuctionLot(self, driver):
        try:
            driver.implicitly_wait(5)
            assert driver.current_activity == '.shop.goods.ui.AddGoodsActivity'
            PageTitle = driver.find_element_by_id('cn.dcpai.auction:id/tv_title')
            assert PageTitle.text == '新增宝贝'
            SureButton = driver.find_element_by_id('cn.dcpai.auction:id/tv_add')
            # 添加图片按钮
            add_picture = driver.find_element_by_id('cn.dcpai.auction:id/item_img')
            add_picture.click()
            assert driver.current_activity == 'com.lzy.imagepicker.ui.ImageGridActivity'
            CheckBoxList = driver.find_elements_by_id('cn.dcpai.auction:id/cb_check')
            for i in range(len(CheckBoxList) - 4):
                CheckBoxList[i].click()
            driver.find_element_by_id('cn.dcpai.auction:id/btn_ok').click()
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, '名称不能为空') == True
                print(f'只添加图片后添加商品，功能正常')
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            # 添加名字
            add_name = driver.find_element_by_id('cn.dcpai.auction:id/et_name')
            add_name.clear()
            add_name.send_keys(PulicClass().Chinese(5))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "商品简介不能为空") == True
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            # 简介
            desc_loc = (By.ID, "cn.dcpai.auction:id/et_desc")
            PulicClass().up_swipe_to_display(driver, *desc_loc)
            add_lot_desc = driver.find_element_by_id('cn.dcpai.auction:id/et_desc')
            add_lot_desc.clear()
            add_lot_desc.send_keys(PulicClass().Chinese(30))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "加价幅度不能为空") == True
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            # 设置起拍价
            BeginPriceLoc = (By.ID, "cn.dcpai.auction:id/et_begin_price")
            PulicClass().up_swipe_to_display(driver, *BeginPriceLoc)
            add_lot_beginprice = driver.find_element_by_id('cn.dcpai.auction:id/et_begin_price')
            add_lot_beginprice.clear()
            PulicClass().Press_keycode(driver, random.randint(0, 100))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "加价幅度不能为空") == True
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            PulicClass().randow_hight_swipe(driver, 400)
            # 添加市场估价
            add_lot_markervalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
            add_lot_markervalue.clear()
            PulicClass().Press_keycode(driver, random.randint(1000, 10000))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "加价幅度不能为空") == True
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            # 加价幅度
            add_lot_invalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_bid_inc_value')
            add_lot_markervalue.clear()
            PulicClass().Press_keycode(driver, random.randint(1000, 10000))
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "藏品类别不能为空") == True
            except:
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
            # 添加拍品类型
            add_lot_type = driver.find_element_by_id('cn.dcpai.auction:id/tv_type')
            add_lot_type.click()
            TimeList = driver.find_elements_by_class_name('android.widget.TextView')
            [driver.drag_and_drop(TimeList[-1], TimeList[int(len(TimeList) / 2)]) for i in range(2)]
            driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            SureButton.click()
            try:
                assert PulicClass().Toast(driver, "宝贝添加成功") == True
                ContinueAdd = WebDriverWait(driver, 2).until\
                    (EC.visibility_of_element_located(
                        (By.XPATH, "//*[contains(@text, '继续添加') and contains(@class, 'android.widget.Button')]")))
                Esc = WebDriverWait(driver, 2).until\
                    (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '继续添加')]")))
                print(f'添加秒啪商品成功')
                Esc.click()
            except:
                print(f'添加秒啪商品失败')
                driver.save_screenshot(IMG_PATH + r'\AddDelayAuctionLot_%s.png' % self.Day)
                pass
        except:
            print(f'添加秒啪商品功能存在问题')
            assert True == False

    # 编辑更新轰啪商品
    def check_update_auctionLot(self, driver, lotId):
        req = Down_V5Api().updateMyAppProductInit_270(lotId)
        try:
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.AddBabyActivity'
            # 保存按钮
            SaveButton = driver.find_element_by_id('cn.dcpai.auction:id/btn_right')
            # 名字
            add_name = driver.find_element_by_id('cn.dcpai.auction:id/et_name')
            assert add_name.text == req.json()['name']
            # 拍卖时长
            add_lot_time = driver.find_element_by_id('cn.dcpai.auction:id/tv_plan_time_key')
            assert add_lot_time.text == req.json()['planTimeValue']
            # 市场估价
            add_lot_markervalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_market_price_value')
            assert add_lot_markervalue.text == req.json()['marketPriceValue']
            # 藏品类型
            add_lot_type = driver.find_element_by_id('cn.dcpai.auction:id/tv_type')
            assert add_lot_type.text == req.json()['typeValue']
            cmd(driver).up_swipe()
            # 起拍价
            add_lot_beginprice = driver.find_element_by_id('cn.dcpai.auction:id/et_begin_price')
            assert float(''.join(re.findall('\d', add_lot_beginprice.text.replace(',', '')))) == \
                   float(req.json()['beginPrice'])
            # 加价幅度
            add_lot_bidvalue = driver.find_element_by_id('cn.dcpai.auction:id/tv_bid_inc_value')
            assert float(''.join(re.findall('\d', add_lot_bidvalue.text.replace(',', '')))) == \
                   float(req.json()['bidIncValue'])
            cmd(driver).down_swipe()
            self.add_auctionLot(driver)
        except:
            print(f'更新商品功能存在问题')
            pass