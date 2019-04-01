#!user/bin/python
#-*- coding: utf-8 -*-
__author__:'huangsonglin@dcpai.cn'
__version__:'1.0'
__CreatrDate__:'2018/11/5 16:15'
__Description__:'主要构建AndroidDeiver'


from appium import webdriver
from Until.YamlRead import *
from selenium.webdriver.common.by import By
from adb_command.adb import *

class Driver:
    def __init__(self):
        self.devicename = ADB().get_devicename()
        self.desired_capabilities = {}
        # 测试平台设置
        self.desired_capabilities['platformName'] = 'Android'
        # 测试包的绝对路径--如果设置包名称和activity后这个可以不要
        self.desired_capabilities['app'] = APK_PATH
        # 手机系统版本
        self.desired_capabilities['platformVersion'] = ADB().get_system()
        # 测试包的mainactivity--(启动app时的activity)
        self.desired_capabilities['appActivity'] = 'cn.dcpai.auction.SplashActivity'
        self.desired_capabilities['appWaitActivity'] = 'cn.dcpai.auction.MainActivity'
        # 测试包名称
        self.desired_capabilities['appPackage'] = 'cn.dcpai.auction'
        # Appium服务器待appium客户端发送新消息的时间。默认为60秒
        self.desired_capabilities['newCommandTimeout'] = '20'
        # 指定运行手机ID运行
        self.desired_capabilities['deviceName'] = self.devicename
        # true:不重新安装APP，false:重新安装app
        self.desired_capabilities['noReset'] = True
        self.desired_capabilities['automationName '] = 'uiautomator2'
        self.desired_capabilities['unicodeKeyboard'] = 'true'  # 是否支持unicode的键盘。如果需要输入中文，要设置为“true”
        self.desired_capabilities['resetKeyboard'] = 'true'  # 是否在测试结束后将键盘重新设置为系统默认的输入法。
        # appium中设置的代理
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.desired_capabilities)
        self.driver.implicitly_wait(10)

    def get_driver(self):
        return self.driver



