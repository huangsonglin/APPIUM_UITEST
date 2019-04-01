#!user/bin/python
#-*-coding:utf-8 -*-
__author__:'huangsonglin@dcpai.cn'

from Driver.Driver import *
from Command import command
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Until.YamlRead import *
from adblogcat.logcat import *


class Login_Class(command.command):

    # 进入我的页面
    def into_user_page(self):
        ele_mine = (By.ID, (Config(HomePage).get('mine_RadioButton')))
        self.click(*ele_mine)

    # 进入账号登录界面
    def into_mobilelogin(self):
        ele_user_login = (By.ID, (Config(LoginPage).get('mobile_login')))
        self.click(*ele_user_login)
        assert self.get_current_activity() == Config(ActivityPath).get('MobileLogin')

    # 账号登录
    def Mobile_Login(self, username, password):
        ele_username = (By.ID, (Config(LoginPage).get('phone_num')))
        ele_pasword = (By.ID, (Config(LoginPage).get('password')))
        ele_login = (By.ID, (Config(LoginPage).get('login_button')))
        self.send_keys(username, *ele_username)
        self.send_keys(password, *ele_pasword)
        self.click(*ele_login)


    # 是否登录
    def is_login(self):
        if self.get_current_activity() == Config(ActivityPath).get('Main'):
            return True
        else:
            return False

    # 是否登录成功
    def is_successful_login(self):
        if self.get_current_activity() != Config(ActivityPath).get('Main'):
            return False
        else:
            try:
                assert self.get_current_activity() == Config(ActivityPath).get('Main')
                ele_username = (By.ID, (Config(MinePage).get("user_nickname")))
                ele_setting = (By.ID, (Config(MinePage).get("setting_button")))
                ele_userIcon = (By.ID, (Config(MinePage).get("user_icon")))
                ele_dcnum = (By.ID, (Config(MinePage).get("user_dcnum")))
                assert self.is_elementExits(*ele_username) == True
                assert self.is_elementExits(*ele_setting) == True
                assert self.is_elementExits(*ele_userIcon) == True
                assert self.is_elementExits(*ele_dcnum) == True
                return True
            except Exception as e:
                return False

    # 退出登录
    def logout(self):
        ele_setting = (By.ID, (Config(MinePage).get('setting_button')))
        ele_logout = (By.ID, (Config(MinePage).get('logout')))
        self.click(*ele_setting)
        time.sleep(1)
        assert self.get_current_activity() == Config(ActivityPath).get('Setting')
        self.click(*ele_logout)
        self.implicitly_wait(1)
        assert self.get_current_activity() == Config(ActivityPath).get('Main')

    # 获取token
    def refresh(self):
        get_log()
        self.find_element_by_id('tv_my_order').click()
        time.sleep(10)
        self.implicitly_wait(2)
        self.back()
        end_log()
        get_Token()

if __name__ == '__main__':
    dr = Driver().get_driver()
    Login_Class(dr).into_user_page()
    if Login_Class(dr).is_login():
        Login_Class(dr).refresh()
    else:
        get_log()
        Login_Class(dr).into_mobilelogin()
        Login_Class(dr).Mobile_Login(13988888001, 123456)
        end_log()
        get_Login_token()
        time.sleep(2)
        successful = Login_Class(dr).is_successful_login()
        assert successful == True




