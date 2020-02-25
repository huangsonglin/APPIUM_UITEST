#!user/bin/python
#-*- coding: utf-8 -*-
__author__:'huangsonglin@dcpai.cn'
__version__:'1.0'
__CreatrDate__:'2018/11/5 16:15'
__Description__:'Mainly encapsulates related apis'

from Driver.driver import *
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class ElementError:
    pass


class PublicShell:

    def __init__(self, driver):
        self.driver = driver

    # 获取手机屏幕尺寸
    def get_size(self):
        result = self.driver.get_window_size()
        return result

    # 查找元素--显示查找
    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver,timeout=10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except Exception as e:
            raise e

    # 左滑动操作
    def left_swipe(self):
        '''
        :param start_x: 开始滑动X坐标
        :param start_y: 开始滑动Y坐标
        :param end_x:   滑动结束X坐标
        :param duration：持续滑动时间
        :return:
        '''
        result = self.get_size()
        x = result['width']
        y = result['height']
        self.driver.swipe(x*3/4, y/2, x/4, y/2, duration=1000)

    # 右滑动操作
    def right_swipe(self):
        result = self.get_size()
        x = result['width']
        y = result['height']
        self.driver.swipe(x/5, y/2, 4*x/5, y/2, duration=1000)

    # 向上滑动
    def up_swipe(self):
        result = self.get_size()
        x = result['width']
        y = result['height']
        self.driver.swipe(x/2, y*4/5, x/2, y/5, duration=1000)

    # 向下滑动
    def down_swipe(self):
        result = self.get_size()
        x = result['width']
        y = result['height']
        self.driver.swipe(x/2, y/5, x/2, y*4/5, duration=1000)

    # 元素是否存在
    def is_elementExits(self, *loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
            Flag = True
        except:
            Flag = False
        finally:
            return Flag





