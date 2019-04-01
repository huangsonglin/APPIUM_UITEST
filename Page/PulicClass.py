#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/11 11:20'

import os,sys
import time
import re,random
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command
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
from appium.webdriver.common.touch_action import TouchAction
from adblogcat.logcat import *
import math, cmath

class PulicClass:

    username = Config(CONFIG_FILE).get('username')
    password = Config(CONFIG_FILE).get('password')
    Day = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def Login(self, driver):
        Login_Class(driver).into_user_page()
        if Login_Class(driver).is_login():
            Login_Class(driver).refresh()
        else:
            get_log()
            Login_Class(driver).into_mobilelogin()
            Login_Class(driver).Mobile_Login(self.username, self.password)
            end_log()
            get_Login_token()
            successful = Login_Class(driver).is_successful_login()
            assert successful == True

    # 点击切换到首页
    def Into_HomePage(self, driver):
        try:
            ele = 'cn.dcpai.auction:id/main_page'
            HomeButton = driver.find_element_by_android_uiautomator(f'new UiSelector().resourceId("{ele}")')
            HomeButton.click()
            time.sleep(1)
        except:
            raise '进入首页失败'

    # 点击切换到龖*竞拍界面
    def Into_Da_Auction(self, driver):
        try:
            ele = 'cn.dcpai.auction:id/special_auction'
            Da_Auction_Buttion = driver.find_element_by_android_uiautomator(f'new UiSelector().resourceId("{ele}")')
            Da_Auction_Buttion.click()
            time.sleep(1)
        except:
            raise '进入龖*竞拍页面失败'

    # 进入龖*江湖界面
    def Into_Da_JiangHu(self, driver):
        try:
            ele = 'cn.dcpai.auction:id/jianghu'
            Da_JiangHu_Buttion = driver.find_element_by_android_uiautomator(f'new UiSelector().resourceId("{ele}")')
            Da_JiangHu_Buttion.click()
            time.sleep(1)
        except:
            raise '进入龖*江湖页面失败'

    # 进入龖* 商城界面
    def Into_Da_Shop(self, driver):
        try:
            ele = 'cn.dcpai.auction:id/main_mall'
            Da_Shop_Buttion = driver.find_element_by_android_uiautomator(f'new UiSelector().resourceId("{ele}")')
            Da_Shop_Buttion.click()
            time.sleep(1)
        except:
            raise '进入龖*商城页面失败'

    # 进入我的页面
    def Into_Mine(self, driver):
        try:
            ele = 'cn.dcpai.auction:id/mine'
            Mine_Buttion = driver.find_element_by_android_uiautomator(f'new UiSelector().resourceId("{ele}")')
            Mine_Buttion.click()
            time.sleep(1)
        except:
            raise '进入龖*商城页面失败'

    def WBShare(self, driver):
        driver.implicitly_wait(5)
        ShareButton = driver.find_element_by_id('topic_detail_share_im')
        ShareButton.click()
        driver.implicitly_wait(5)
        assert driver.find_element_by_id('textView7').text == '分享到'
        WBShare = driver.find_element_by_id('weibo')
        Collect = driver.find_element_by_id('share_collection_tv')
        Inform = driver.find_element_by_id('share_report_tv')
        WBShare.click()
        driver.implicitly_wait(5)
        assert current_package() == 'com.sina.weibo'
        driver.back()

    def WXShare(self, driver):
        driver.implicitly_wait(5)
        ShareButton = driver.find_element_by_id('topic_detail_share_im')
        ShareButton.click()
        driver.implicitly_wait(5)
        assert driver.find_element_by_id('textView7').text == '分享到'
        WXShare = driver.find_element_by_id('weixin_haoyou')
        WXShare.click()
        if 'com.tencent.mm' in ADB().getList():
            assert current_package() == 'com.tencent.mm'
            driver.back()
            assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'
            driver.back()
        else:
            assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'

    def WXQShare(self, driver):
        driver.implicitly_wait(5)
        ShareButton = driver.find_element_by_id('topic_detail_share_im')
        ShareButton.click()
        driver.implicitly_wait(5)
        assert driver.find_element_by_id('textView7').text == '分享到'
        WXQShare = driver.find_element_by_id('weixin_quan')
        WXQShare.click()
        if 'com.tencent.mm' in ADB().getList():
            assert current_package() == 'com.tencent.mm'
            driver.back()
        else:
            assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'

    def QQShare(self, driver):
        ShareButton = driver.find_element_by_id('topic_detail_share_im')
        ShareButton.click()
        driver.implicitly_wait(5)
        assert driver.find_element_by_id('textView7').text == '分享到'
        QQShare = driver.find_element_by_id('share_qq_zone')
        QQShare.click()

    def Chinese(self, num):
        ChinsesChr = ''
        for i in range(num):
            val = random.randint(0x4e00, 0x9fbf)
            ChinsesChr += chr(val)
        return ChinsesChr

    # 拍品|拍场分享
    def ShareIntoWebio(self, driver):
        try:
            SHAREBUTTON = driver.find_element_by_android_uiautomator \
                ('new UiSelector().resourceId("cn.dcpai.auction:id/title_share_btn")')
            SHAREBUTTON.click()
            time.sleep(1)
            driver.implicitly_wait(2)
            WEIBOBUTTON = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '微博')]")))
            WEIBOBUTTON.click()
            time.sleep(2)
            driver.implicitly_wait(5)
            assert current_package() == 'com.sina.weibo'
            driver.back()
            try:
                WebDriverWait(driver, timeout=3).until \
                    (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '是否保存草稿')]")))
                driver.find_element_by_android_uiautomator('new UiSelector().text("不保存")').click()
            except:
                pass
        except:
            assert True == False

    def ShareIntoWeiXin(self, driver):
        try:
            SHAREBUTTON = driver.find_element_by_android_uiautomator\
                ('new UiSelector().resourceId("cn.dcpai.auction:id/title_share_btn")')
            SHAREBUTTON.click()
            driver.implicitly_wait(2)
            time.sleep(1)
            WEIXINBUTTON = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '微信好友')]")))
            WEIXINBUTTON.click()
            driver.implicitly_wait(5)
            if 'com.tencent.mm' in ADB().getList():
                assert current_package() in ['com.tencent.mm','com.huawei.android.internal.app']
                driver.back()
            else:
                assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'
        except:
            assert True == False

    def ShareIntoWeiXinQuan(self, driver):
        try:
            SHAREBUTTON = driver.find_element_by_android_uiautomator \
                ('new UiSelector().resourceId("cn.dcpai.auction:id/title_share_btn")')
            SHAREBUTTON.click()
            driver.implicitly_wait(2)
            time.sleep(1)
            WEIXINQUANBUTTON = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '朋友圈')]")))
            WEIXINQUANBUTTON.click()
            driver.implicitly_wait(5)
            time.sleep(2)
            if 'com.tencent.mm' in ADB().getList():
                # 后者为微信使用了分身
                assert current_package() in ['com.tencent.mm','com.huawei.android.internal.app']
                driver.back()
            else:
                assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'
        except:
            assert True == False

    def ShareIntoDAJIANGHU(self, driver):
        try:
            SHAREBUTTON = driver.find_element_by_android_uiautomator \
                ('new UiSelector().resourceId("cn.dcpai.auction:id/title_share_btn")')
            SHAREBUTTON.click()
            driver.implicitly_wait(2)
            time.sleep(1)
            DAJIANGHU = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '朋友圈')]")))
            DAJIANGHU.click()
            driver.implicitly_wait(5)
            time.sleep(2)
            assert driver.current_activity == '.activity.ShareToJianghuActivity'
            Title = WebDriverWait(driver, timeout=5).until\
                (EC.visibility_of_element_located((By.ID, 'tv_title')))
            assert Title.text == '分享话题'
            driver.back()
        except:
            assert True == False

    # 获取toast信息
    def Toast(self, driver, message):
        try:
            Toast = WebDriverWait(driver, timeout=3).until\
                (EC.visibility_of_element_located((By.XPATH, f"//*[contains(@text, '{message}')]")))
            return True
        except:
            return False

    # 输入纯数字
    def Press_keycode(self, driver, Number):
        try:
            for i in range(len(str(Number))):
                num = int(str(Number)[i])
                driver.press_keycode(num + 7)
                time.sleep(0.5)
        except Exception as e:
            raise e

    # 模拟手指点击
    def Tap(self, driver, ele):
        Higet = ele.size['height']
        Width = ele.size['width']
        Start_X = ele.location['x']
        Start_Y = ele.location['y']
        driver.tap([(int((Start_X + Width)/2), int((Start_Y + Higet)/2))], 500)

    def get_box(self, driver, ele):
        Higet = ele.size['height']
        Width = ele.size['width']
        Start_X = ele.location['x']
        Start_Y = ele.location['y']
        box = (Start_X, Start_Y, Start_X+Width, Start_Y+Higet)
        return box

    # 退出拍卖现场
    def quit_auction(self, driver):
        try:
            driver.back()
            AlertToast = WebDriverWait(driver, 10, 0.5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'alertTitle')]")))
            QUIT = driver.find_element_by_android_uiautomator('new UiSelector().resourceId("android:id/button1")')
            QUIT.click()
        except Exception as e:
            raise e

    def touch_tap(self, driver, ele):
        TouchAction(driver).tap(ele).perform()

    # 向上滑动元素至可见
    def up_swipe_to_display(self, driver, *loc):
        result = driver.get_window_size()
        x = result['width']
        y = result['height']
        for i in range(math.ceil(y / 10)):
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located(loc))
                break
            except:
                driver.swipe(x/2, y*4/5, x/2, y*7/10, duration=1000)

    # 向下滑动至元素可见
    def down_swipe_to_display(self, driver, *loc):
        result = driver.get_window_size()
        x = result['width']
        y = result['height']
        for i in range(math.ceil(y / 10)):
            try:
                ele = WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located(loc))
                break
            except Exception as e:
                driver.swipe(x / 2, y*3/5, x / 2, y/4, 1000)

    # 滑动
    def swipe_random_up(self, driver, Y):
        result = driver.get_window_size()
        x = result['width']
        y = result['height']
        driver.swipe(x / 2, y /2 + (Y), x / 2, y / 2, 1000)

    # 上下任意滑动
    def randow_hight_swipe(self, driver, Y):
        result = driver.get_window_size()
        x = result['width']
        y = result['height']
        if isinstance(Y, int):
            driver.swipe(x / 2, y / 2 + (Y), x / 2, y / 2, 1000)
        else:
            error = '请输入正确的值'
            raise error


    # 拖动元素至某个坐标
    def touch_swipe(self, driver, ele, x, y):
        TouchAction(driver).long_press(ele).move_to(None, x, y).release().perform()

    # 取消当前界面所有的提示信息
    def Esc_Alert(self, driver):
        try:
            PushBox = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'parentPanel')]")))
            LookButton = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[@text='去看看]')]")))
            ESCButton = WebDriverWait(driver, timeout=5).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[@text='取消]')]")))
            ESCButton.click()
        except:
            pass

    # 截图保存
    def save_img(self, driver, filename):
        try:
            driver.save_screenshot(IMG_PATH + f'\%s.png' %(str(filename)+self.Day))
        except:
            error = '图片保存失败'
            raise error

    def new_toast(self, driver, message):
        try:
            driver.find_element_by_android_uiautomator('new UiSelector().textContains("%s")' % str(message))
            return True
        except:
            return False
