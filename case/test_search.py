#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/12/20 11:35'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from appium.webdriver.common import mobileby
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Driver.driver import AndroidDriver
import time
import unittest
import math
from adblogcat.logcat import *
from Until.DB import Mysql
from Until.YamlRead import *
from command.driver_command import DirvrCommand
from Public.Fuction import CCUtility
from API.V5down import Four_Vesion_Api

class Test_Search(unittest.TestCase):
	def setUp(self):
		pass

	@classmethod
	def setUpClass(cls):
		cls.driver = AndroidDriver().AndriodDriver()
		cls.name = datetime.datetime.now().strftime('%m%d')
		cls.logpath = f'{Logcat}\%s.txt' % cls.name

	@classmethod
	def tearDownClass(cls):
		pass

	def tearDown(self):
		pass

	def test_001_init_search(self):
		try:
			ele_search_btn = self.driver.find_element(By.ID, "home_layout_search_btn")
			ele_search_btn.click()
			self.assertEqual(self.driver.current_activity, ".activity.JianghuSearchWebViewActivity", msg="搜索页面activity正常")
			search_text = WebDriverWait(self.driver, 10, 0.01).until(EC.visibility_of_element_located((By.XPATH, "//*[@text='热门搜索']")))
			# 话题
			topic_bar = self.driver.find_element_by_id('toppic_radio_button')
			# 藏品
			collection_bar = self.driver.find_element_by_id('collection_radio_button')
			# 藏友
			friden_bar = self.driver.find_element_by_id('friden_radio_button')
			# 门派
			guild_bar = self.driver.find_element_by_id('guild_radio_button')
			self.assertEqual(topic_bar.get_attribute('checked'), "true", msg="初始页面话题默认被选中")
			# 热门搜索内容
			hot_search_text = self.driver.find_elements_by_xpath('//*[@resource-id="cn.dcpai.auction:id/gridView_hot"]/android.widget.TextView')
			# 数据库存储热门搜索内容
			database_search_text = Mysql().sql_result('SELECT `value` from param WHERE `type`="HOT_SEARCH_KEYWORD" ORDER BY param_order')
			self.assertEqual(len(hot_search_text), len(database_search_text), msg="热搜内容个数和数据库一致")
			for i in range(len(database_search_text)):
				hot_text = hot_search_text[i].text
				db_hot_text = database_search_text[i][0]
				self.assertEqual(hot_text, db_hot_text, msg="热搜内容一致")
		except Exception as e:
			raise e

	# 搜索话题
	def test_002_search_topic(self):
		try:
			# txt = CCUtility().random_name(1)
			txt = "一"
			ele_search_txt = self.driver.find_element_by_id('search_src_text')
			ele_search_txt.clear()
			ele_search_txt.send_keys(txt)
			# enter键确认
			self.driver.press_keycode(66)
			self.assertEqual(self.driver.current_activity, ".activity.JianghuSearchWebViewActivity", msg="搜索结果acitivity正确")
			req = Four_Vesion_Api().searchPostPage_300(txt)
			resutl = req.json()['rows']
			# 搜索结果列表页
			search_list_view = self.driver.find_element_by_id('cn.dcpai.auction:id/search_result_list_view')
			search_list_view_size = search_list_view.size
			init_hight = search_list_view.location['y']
			one_result_view = search_list_view.find_elements_by_class_name('android.widget.LinearLayout')
			# 单个搜索结果
			one_result_view_size = one_result_view[0].size
			# 每行展示的个数
			row_num = search_list_view_size['width'] / one_result_view_size['width']
			# 当前可见个数
			visible_all_number = int(search_list_view_size['height'] / one_result_view_size['height']) * row_num
			visible_all_number = int(visible_all_number)
			topic_result_list = []
			for i in range(len(resutl)):
				for result_view in one_result_view:
					try:
						ele_title = result_view.find_element_by_xpath("//*[@resource-id='cn.dcpai.auction:id/search_post_title']")
						print(ele_title.text)
					except:
						pass
				if i % (visible_all_number -1) == 0 and i != 0:
					self.driver.swipe(one_result_view_size['width'], one_result_view[visible_all_number -1].location['y'] + one_result_view_size['height'], one_result_view_size['width'], init_hight-20, duration=3000)
		except Exception as e:
			raise e

if __name__ == '__main__':
    unittest.main()