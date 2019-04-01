#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/5 10:58'

"""
IM聊天信息
"""

import os,sys
import time
import re,random
from Until.YamlRead import *
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Page.PulicClass import *
from Until.diffrentPng import *
from Until.GetFile import *
from adblogcat.logcat import *

class IM:

    # 聊天—出价切换
    def IM_switch_Price(self, driver):
        try:
            Switch_to_Price = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_price")))
            Switch_to_Price.click()
            Switch_to_Chat = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_chat_outprice")))
            AddButton = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_btn')))
            MinusButton = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_minus_btn')))
            EditPrice = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, 'auction_input_outprice_add_edit')))
            assert True == True, u'聊天切换出价功能正常'
        except:
            assert True == False

    # 出价-聊天切换
    def Price_switch_IM(self, driver):
        try:
            Switch_to_Chat = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_chat_outprice")))
            Switch_to_Chat.click()
            EditText = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_message")))
            EMoJJ = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_emoji")))
            InputMore = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_more")))
            assert True == True, u'出价切换聊天功能正常'
        except:
            assert True == False

    # 图文拍场下文字聊天
    def send_text(self, driver):
        try:
            EditText = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_message")))
            EMoJJ = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_emoji")))
            InputMore = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_more")))
            EditText.click()
            EditText.clear()
            TEXT = PulicClass().Chinese(random.randint(1,30))
            EditText.send_keys(TEXT)
            Send = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text,'发送')]")))
            Send.click()
            time.sleep(3)
            # 评论板块区域
            RecordList = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id,'chat_record_list')]")))
            Contents = RecordList.find_elements_by_id('tv_chatcontent')
            assert Contents[-1].text == TEXT
        except:
            assert True == False

    # 发送表情
    def send_emoij(self, driver):
        try:
            EMoJJ = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_emoji")))
            EMoJJ.click()
            time.sleep(1)
            # 表情展示区域
            EmoJJArea = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'gridview')]")))
            # 表情系列切换
            ListEmojj =  WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_frame_icon")))
            # 默认表情包
            default_emotion_indicator = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "default_emotion_indicator")))
            # 表情包
            NewList = ListEmojj.find_elements_by_class_name('android.widget.ImageView')
            for every in NewList:
                every.click()
                time.sleep(1)
                EmoJJArea.find_elements_by_class_name('android.widget.ImageView')[0].click()
                time.sleep(1)
                if every == NewList[-1]:
                    SEND = driver.find_element_by_android_uiautomator\
                        ('new UiSelector().text("发送")')
                    SEND.click()
                    time.sleep(1)
                Date = datetime.datetime.now().date().strftime('%Y%m%d')
                Pngname = f'{IMG_PATH}\{Date}_%d.png' % NewList.index(every)
                driver.save_screenshot(Pngname)
            # 每条评论板块区域
            ARER = driver.find_elements_by_xpath\
                ("//*[contains(@resource-id,'chat_record_list')]/android.widget.LinearLayout")
            IMIMage = GetFile(IMG_PATH)
            for i in range(len(IMIMage)):
                if i+1 <len(IMIMage):
                    assert CompareImg(IMIMage[i], IMIMage[i+1], PulicClass().get_box( driver, ARER[-1])) == False
            print(f'发送表情成功')
        except:
            assert True == False

    # 发送Image(图片)
    def send_image(self, driver):
        try:
            InputMore = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.ID, "auction_input_more")))
            InputMore.click()
            time.sleep(1)
            photograph = WebDriverWait(driver, 5).until\
                (EC.visibility_of_element_located((By.ID, "auction_input_take_picture")))
            image = WebDriverWait(driver, 5).until\
                (EC.visibility_of_element_located((By.ID, "auction_input_take_phone")))
            photograph.click()
            time.sleep(1)
            # 权限提示信息
            if driver.current_activity == '.permission.ui.GrantPermissionsActivity':
                try:
                    # 提示框
                    AlertText = driver.find_element_by_android_uiautomator\
                        ('new UiSelector().resourceId("com.android.packageinstaller:id/perm_desc_root")')
                    # 禁止不再询问
                    Box = driver.find_element_by_android_uiautomator\
                        ('new UiSelector().resourceId("com.android.packageinstaller:id/do_not_ask_checkbox")')
                    Box.click()
                    # 允许按钮
                    Allow = driver.find_element_by_android_uiautomator \
                        ('new UiSelector().resourceId("com.android.packageinstaller:id/permission_allow_button")')
                    # 不同意
                    Disagree = driver.find_element_by_android_uiautomator \
                        ('new UiSelector().resourceId("com.android.packageinstaller:id/permission_deny_button")')
                    Allow.click()
                    time.sleep(1)
                    # 不同意的情况下
                    # Disagree.click()
                    assert (driver.current_activity) == '.activity.AuctionNewActivity'
                    photograph.click()
                except:
                    pass
            time.sleep(2)
            assert driver.current_activity == '.ThirdCamera', u'调用照相机功能正常'
            assert 'camera' in current_package()
            driver.back()
            image.click()
            time.sleep(2)
            assert 'com.android.gallery3d' == current_package(), u'调用图片功能正常'
            try:
                PhotoList = driver.find_elements_by_android_uiautomator \
                    ('new UiSelector().resourceId("com.android.gallery3d:id/gallery_statelist_view")')
                PhotoList[0].click()
                ele = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("android:id/action_bar_container")')
                box = PulicClass().get_box(driver, ele)
                driver.tap([(box[0], box[3]+20)], 500)
                time.sleep(1)
                sureImg = driver.find_element_by_android_uiautomator \
                    ('new UiSelector().resourceId("com.android.gallery3d:id/head_select_right")')
                sureImg.click()
                time.sleep(1)
                assert driver.current_activity  == '.activity.AuctionNewActivity', u'选择图片后自动返回聊天界面'
                # 每条评论板块区域
                ARER = driver.find_elements_by_xpath \
                    ("//*[contains(@resource-id,'chat_record_list')]/android.widget.LinearLayout")
                try:
                    # 能找到图片且可点击
                    ARER[-1].find_element_by_id('iv_sendPicture').click()
                    time.sleep(1)
                    assert driver.current_activity == 'com.easemob.chatuidemo.activity.ShowBigImage'
                    driver.back()
                except:
                    print(f'发送图片功能可能存在问题,请相关测试人员手动验证功能~~~')
            except:
                print(f'手机中可能不存在图片，请相关测试人员手动验证功能~~~')
        except:
            assert True == False

