#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/12/25 17:20'

import os
import sys
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from appium.webdriver.common import mobileby
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Driver.driver import AndroidDriver
import time
import math
import random
from Until.YamlRead import *
from command.driver_command import PublicShell
from Public.Fuction import Public_Function
from API.V5down import Four_Vesion_Api


class Test_Bannner():

	def setup_module(self):
		pass

	@classmethod
	def setup_class(cls):
		cls.driver = AndroidDriver().driver

	@classmethod
	def teardown_class(cls):
		cls.driver.quit()

	def teardown_module(self):
		pass

	def test_001_home_banner(self):
		"""首页顶部banner"""
		try:
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P4")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) >1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH,'//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME,'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height']/2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
		except Exception as e:
			raise e

	def test_002_Dashop_product_banner(self):
		"""龖商城-商品顶部banner"""
		try:
			shop_button = self.driver.find_element(By.ID, "main_mall")
			shop_button.click()
			self.driver.implicitly_wait(10)
			product_element = self.driver.find_element_by_id('tv_goodslist')
			product_element.click()
			time.sleep(0.5)
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P11")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) > 1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME, 'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height'] / 2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
		except Exception as e:
			raise e

	def test_003_Dashop_shop_banner(self):
		"""龖商城-店家顶部banner"""
		try:
			shop_button = self.driver.find_element(By.ID, "main_mall")
			shop_button.click()
			self.driver.implicitly_wait(10)
			product_element = self.driver.find_element_by_id('tv_goodslist')
			product_element.click()
			time.sleep(0.5)
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P12")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) > 1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME, 'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height'] / 2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
		except Exception as e:
			raise e

	def test_004_Guild_choiceness_banner(self):
		"""龖江湖-精选顶部banner"""
		try:
			bbs_button = self.driver.find_element(By.ID, "jianghu")
			bbs_button.click()
			self.driver.implicitly_wait(10)
			time.sleep(0.5)
			content = PublicShell(self.driver).is_elementExits(By.ID, "topic_join_LinearLayout")	# 首次进入提示
			if content:
				alret_esc = self.driver.find_element_by_id("jorum_close_im")
				alret_esc.click()
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P13")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) > 1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME, 'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height'] / 2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
		except Exception as e:
			raise e

	def test_005_Guild_video_banner(self):
		"""龖江湖-视频页顶部banner"""
		try:
			bbs_button = self.driver.find_element(By.ID, "jianghu")
			bbs_button.click()
			self.driver.implicitly_wait(10)
			time.sleep(0.5)
			content = PublicShell(self.driver).is_elementExits(By.ID, "topic_join_LinearLayout")	# 首次进入提示
			if content:
				alret_esc = self.driver.find_element_by_id("jorum_close_im")
				alret_esc.click()
			video = self.driver.find_element_by_id('select_tv_video')	# 视频按钮
			video.click()
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P13")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) > 1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME, 'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height'] / 2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
		except Exception as e:
			raise e

	# 直播页面
	def test_006_Living_banner(self):
		"""直播页顶部banner"""
		try:
			home = self.driver.find_element(By.ID, "main_page")
			home.click()
			self.driver.implicitly_wait(10)
			time.sleep(0.5)
			living_button = self.driver.find_element_by_id('home_live')
			living_button.click()
			self.driver.implicitly_wait(10)
			time.sleep(0.5)
			assert self.driver.current_activity == '.live.ui.LiveListActivity'
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '全部')]") == True
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '轰啪')]") == True
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '秒啪')]") == True
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '讲堂')]") == True
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '巡展直播')]") == True
			req = Four_Vesion_Api().findAdvertiseContent_260(position="P15")
			result = req.json()['appAdvertiseDtoList']
			if len(result) != 0:
				banner_center = self.driver.find_element(By.ID, "bannerContainer")
				banner_image = self.driver.find_element(By.ID, "bannerViewPager")
				if len(result) > 1:
					# banner焦点图
					banner_focus = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"circleIndicator")]')
					banner_focus_list = banner_focus.find_elements(By.CLASS_NAME, 'android.widget.ImageView')
					assert len(banner_focus_list) == len(result), u"首页banner广告数一致"
					for i in range(len(banner_focus_list)):
						banner_image.click()
						self.driver.implicitly_wait(1)
						if self.driver.current_activity == ".MainActivity":
							error_img = os.path.join(IMG_PATH, "home_banner_error.png")
							self.driver.save_screenshot(error_img)
						else:
							self.driver.back()
						x = banner_image.location["x"]
						y = banner_image.location["y"] + int(banner_image.size['height'] / 2)
						x1 = x + banner_image.size['width']
						y1 = y
						self.driver.swipe(x, y, x1, y1)
				else:
					banner_image.click()
					if self.driver.current_activity == ".MainActivity":
						error_img = os.path.join(IMG_PATH, "home_banner_error.png")
						self.driver.save_screenshot(error_img)
					else:
						self.driver.back()
				self.driver.back()	# 退回到主页
		except Exception as e:
			raise e
if __name__ == '__main__':
	pytest.main('-m')
