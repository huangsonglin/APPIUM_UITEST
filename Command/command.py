#!user/bin/python
#-*- coding: utf-8 -*-
__author__:'huangsonglin@dcpai.cn'
__version__:'1.0'
__CreatrDate__:'2018/11/5 16:15'
__Description__:'Mainly encapsulates related apis'

from Driver.Driver import *
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class ElementError:
    pass


class command:

    def __init__(self, driver):
        self.driver = driver

    # 获取手机屏幕尺寸
    def get_size(self):
        # X坐标--宽度
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
    def is_elementExits(self,*loc):
        try:
            WebDriverWait(self.driver, timeout=10).until(EC.visibility_of_element_located(loc))
            element = self.driver.find_element(*loc)
            Flag = True
        except:
            Flag = False
        finally:
            return Flag

    # 点击元素
    def click(self, *loc):
        Flag = self.is_elementExits(*loc)
        if Flag:
            ele = self.find_element(*loc)
            ele.click()
        else:
            raise ElementError('element is not found')

    # 输入文字
    def send_keys(self,value,*loc):
        try:
            self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except Exception as e:
            raise e

    # 通过ID查找元素
    def find_element_by_id(self, id):
        try:
            element = self.driver.find_element_by_id(id)
            return element
        except:
            raise ElementError('Element is not find')

    # 通过xpath属性查找元素
    def find_element_by_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            return element
        except:
            raise ElementError('Element is not find')

    # 获取当前activity
    def get_current_activity(self):
        activity = self.driver.current_activity
        return activity

    # 隐式等待
    def implicitly_wait(self, times):
        self.driver.implicitly_wait(times)

    # 获取元素text
    def get_text(self, ele):
        ele_name = ele.text()
        return ele_name

    # 退出
    def quit(self):
        self.driver.quit()

    # 后退一页
    def back(self):
        self.driver.back()

    # 较小滑动
    def small_up_swipe(self):
        result = self.get_size()
        x = result['width']
        y = result['height']
        self.driver.swipe(x / 2, y * 7/10, x / 2, y*3/5, duration=1000)









