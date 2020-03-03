#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/12/20 11:35'
"""
搜索界面UI测试
"""
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
from selenium.webdriver.common.touch_actions import TouchActions
from Driver.driver import AndroidDriver
import time
import pytest
import math
import random
from adblogcat.logcat import *
from Until.DB import Mysql
from Until.YamlRead import *
from command.driver_command import PublicShell
from Public.Fuction import Public_Function
from API.V5down import Four_Vesion_Api


class Test_Search:

	def setup_module(self):
		pass

	@classmethod
	def setup_class(cls):
		cls.driver = AndroidDriver().driver

	@classmethod
	def teardown_class(cls):
		pass

	def teardown_module(self):
		pass

	def test_001_init_search(self):
		"""搜索默认界面"""
		try:
			ele_search_btn = self.driver.find_element(By.ID, Config(HomePage).get("search_button"))  # 搜索按钮
			ele_search_btn.click()
			assert self.driver.current_activity == ".activity.JianghuSearchWebViewActivity", u"搜索页面activity正常"
			assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='热门搜索']") == True, u'热门搜索存在'
			assert PublicShell(self.driver).is_elementExits(By.ID, "toppic_radio_button") == True, u'话题存在'
			assert PublicShell(self.driver).is_elementExits(By.ID, "collection_radio_button") == True, u'藏品存在'
			assert PublicShell(self.driver).is_elementExits(By.ID, "friden_radio_button") == True, u'藏友存在'
			assert PublicShell(self.driver).is_elementExits(By.ID, "guild_radio_button") == True, u'门派存在'
			topic_bar = self.driver.find_element(By.ID, "toppic_radio_button")
			assert topic_bar.get_attribute('checked') == "true", u"初始页面话题默认被选中"
			# 热门搜索内容
			hot_search_text = self.driver.find_elements_by_xpath \
				('//*[@resource-id="cn.dcpai.auction:id/gridView_hot"]/android.widget.TextView')
			# 数据库存储热门搜索内容
			database_search_text = Mysql().sql_result \
				('SELECT `value` from param WHERE `type`="HOT_SEARCH_KEYWORD" ORDER BY param_order')
			assert len(hot_search_text) == len(database_search_text), u"热搜内容个数和数据库一致"
			for i in range(len(database_search_text)):
				hot_text = hot_search_text[i].text
				db_hot_text = database_search_text[i][0]
				assert hot_text == db_hot_text, u"热搜内容一致"
		except Exception as e:
			raise e

	# 搜索话题
	@pytest.mark.parametrize('content', [(Config(CONFIG_FILE).get("search_content"))])
	def test_002_search_topic(self, content):
		"""话题搜索"""
		try:
			ele_search_txt = self.driver.find_element_by_id('search_src_text')
			ele_search_txt.clear()
			ele_search_txt.send_keys(content)
			# enter键确认
			self.driver.press_keycode(66)
			assert self.driver.current_activity == ".activity.JianghuSearchWebViewActivity", u"搜索结果acitivity正确"
			req = Four_Vesion_Api().searchPostPage_300(content)  # 默认按照热度进行排序
			resutl = req.json()['rows']
			# 搜索结果列表
			search_list_view = self.driver.find_element_by_id('cn.dcpai.auction:id/search_result_list_view')
			search_list_view_size = search_list_view.size
			init_hight = search_list_view.location['y']  # 结果列表页左上方高度
			no_result = PublicShell(self.driver).is_elementExits(By.ID, "error_title")
			if no_result:
				assert req.json() == {"rows": [], "total": "0"}, u"接口内容返回正常"
				result_element = self.driver.find_element(By.ID, "error_title")
				assert "暂无相关" in result_element.text
			else:
				results_list_view = search_list_view.find_elements_by_class_name('android.widget.LinearLayout')
				one_view_size = results_list_view[0].size  # 每个结果的尺寸大小
				row_show_num = int(search_list_view_size['width'] / one_view_size['width'])
				column_show_num = search_list_view_size['height'] / one_view_size['height']  # 可见列数
				column_show_num = round(column_show_num)  # 可见列数(采用四舍五入的方式。因为显示不全可能会导致无法读取数据)
				show_num = row_show_num * column_show_num
				cycle_index = int(len(resutl) / show_num)
				for i in range(cycle_index):
					for j in range(show_num):
						post_title = results_list_view[j].find_element(By.XPATH,
																	   "//*[@resource-id='cn.dcpai.auction:id/search_post_title']").text
						api_post_title = resutl[i * show_num + j]['subject']
						assert post_title == api_post_title, u"话题title展示和接口返回一致"
						post_author = results_list_view[j].find_element(By.XPATH,
																		"//*[contains(@resource-id,'search_post_author_name')]").text
						api_post_author = resutl[i * show_num + j]['memberNickname']
						assert post_author[:6] in api_post_author, u"话题title展示和接口返回一致"
						api_img_num = len(resutl[i * show_num + j]['images'].split(","))
						if api_img_num > 1:
							post_img_num = results_list_view[j].find_element(By.XPATH,
																			 "//*[contains(@resource-id,'search_post_num')]").text
							assert str(api_img_num) == re.findall('[0-9]', post_img_num)[0], u"话题图片数量一致"
						post_onlook_num = results_list_view[j].find_element(By.XPATH,
																			"//*[contains(@resource-id,'search_post_onlooking_count')]").text
						api_post_onlook_num = resutl[i * show_num + j]['observerCount']
						assert post_onlook_num == api_post_onlook_num, u"围观数量一致"
					self.driver.swipe \
						(results_list_view[show_num - 1].location["x"],
						 results_list_view[show_num - 1].location["y"] + one_view_size['height'],
						 results_list_view[show_num - 1].location["x"], init_hight, duration=4000)
					self.driver.implicitly_wait(10)
					time.sleep(4)
			newreq = Four_Vesion_Api().searchPostPage_300(content, sort="N")  # 默认按照热度进行排序
			newresutl = newreq.json()['rows']
			# 最新排序按钮
			new_sort_element = self.driver.find_element(By.ID, "search_post_filter_sort_time")
			new_sort_element.click()
			self.driver.implicitly_wait(10)
			time.sleep(3)
			for i in range(cycle_index):
				for j in range(show_num):
					post_title = results_list_view[j].find_element(By.XPATH,
																   "//*[@resource-id='cn.dcpai.auction:id/search_post_title']").text
					api_post_title = newresutl[i * show_num + j]['subject']
					assert post_title == api_post_title, u"话题title展示和接口返回一致"
					post_author = results_list_view[j].find_element(By.XPATH,
																	"//*[contains(@resource-id,'search_post_author_name')]").text
					api_post_author = newresutl[i * show_num + j]['memberNickname']
					assert post_author[:6] in api_post_author, u"话题title展示和接口返回一致"
					api_img_num = len(newresutl[i * show_num + j]['images'].split(","))
					if api_img_num > 1:
						post_img_num = results_list_view[j].find_element(By.XPATH,
																		 "//*[contains(@resource-id,'search_post_num')]").text
						assert str(api_img_num) == re.findall('[0-9]', post_img_num)[0], u"话题图片数量一致"
					post_onlook_num = results_list_view[j].find_element(By.XPATH,
																		"//*[contains(@resource-id,'search_post_onlooking_count')]").text
					api_post_onlook_num = newresutl[i * show_num + j]['observerCount']
					assert post_onlook_num == api_post_onlook_num, u"围观数量一致"
				self.driver.swipe \
					(results_list_view[show_num - 1].location["x"],
					 results_list_view[show_num - 1].location["y"] + one_view_size['height'],
					 results_list_view[show_num - 1].location["x"], init_hight, duration=4000)
				self.driver.implicitly_wait(10)
				time.sleep(4)
		except Exception as e:
			raise e

	@pytest.mark.skip
	@pytest.mark.parametrize('content', [(Config(CONFIG_FILE).get("search_content"))])
	def test_003_search_filtrate_topic(self, content):
		"""话题搜索--筛选"""
		try:
			filtrate_button = self.driver.find_element(By.ID, "search_post_filter_category")
			filtrate_button.click()
			self.driver.implicitly_wait(10)
			# 筛选类别列表
			type_list_view = self.driver.find_element_by_android_uiautomator \
				('new UiSelector().resourceId("cn.dcpai.auction:id/type_recycler")')
			req = Four_Vesion_Api().findAllPostType_320()
			api_type_list = []
			for result in req.json():
				api_type_list.append(result['name'])
			type_list = type_list_view.find_elements(By.XPATH, "//*[contains(@resource-id, 'type_name')]")
			for every_type in type_list:
				assert every_type.is_enabled() == True
				index = type_list.index(every_type)
				if index == 0:
					assert every_type.text == "全部"
				else:
					assert every_type.text == api_type_list[index - 1]
			random_num = random.randint(1, len(type_list)-1)
			type_list[random_num].click()  # 随机选择一个分类(全部除开)进行查询
			self.driver.implicitly_wait(10)
			time.sleep(4)
			typeReq = Four_Vesion_Api().searchPostPage_300(keyword=content, typeId=random_num, sort="N")
			if typeReq.json()['total'] == '0':
				is_error_toast = PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '暂无相关话题')]")
				assert is_error_toast == True
			else:
				resutl = typeReq.json()['rows']
				search_list_view = self.driver.find_element_by_id('cn.dcpai.auction:id/search_result_list_view')
				search_list_view_size = search_list_view.size
				init_hight = search_list_view.location['y']  # 结果列表页左上方高度
				results_list_view = search_list_view.find_elements_by_class_name('android.widget.LinearLayout')
				one_view_size = results_list_view[0].size  # 每个结果的尺寸大小
				row_show_num = int(search_list_view_size['width'] / one_view_size['width'])
				column_show_num = search_list_view_size['height'] / one_view_size['height']  # 可见列数
				column_show_num = round(column_show_num)  # 可见列数(采用四舍五入的方式。因为显示不全可能会导致无法读取数据)
				show_num = row_show_num * column_show_num
				cycle_index = int(len(resutl) / show_num)
				for i in range(cycle_index):
					for j in range(show_num):
						post_title = results_list_view[j].find_element(By.XPATH,
																	   "//*[contains(@resource-id,'search_post_title')]").text
						api_post_title = resutl[i * show_num + j]['subject']
						assert post_title == api_post_title, u"话题title展示和接口返回一致"
						post_author = results_list_view[j].find_element(By.XPATH,
																		"//*[contains(@resource-id,'search_post_author_name')]").text
						api_post_author = resutl[i * show_num + j]['memberNickname']
						assert post_author[:6] in api_post_author, u"话题title展示和接口返回一致"
						api_img_num = len(resutl[i * show_num + j]['images'].split(","))
						if api_img_num > 1:
							post_img_num = results_list_view[j].find_element(By.XPATH,
																			 "//*[@resource-id='cn.dcpai.auction:id/search_post_num']").text
							assert str(api_img_num) == re.findall('[0-9]', post_img_num)[0], u"话题图片数量一致"
						post_onlook_num = results_list_view[j].find_element(By.XPATH,
																			"//*[contains(@resource-id,'search_post_onlooking_count')]").text
						api_post_onlook_num = resutl[i * show_num + j]['observerCount']
						assert post_onlook_num == api_post_onlook_num, u"围观数量一致"
					self.driver.swipe \
						(results_list_view[show_num - 1].location["x"],
						 results_list_view[show_num - 1].location["y"] + one_view_size['height'],
						 results_list_view[show_num - 1].location["x"], init_hight, duration=4000)
					self.driver.implicitly_wait(10)
					time.sleep(4)
		except Exception as e:
			raise e

	@pytest.mark.parametrize('content', [(Config(CONFIG_FILE).get("search_content"))])
	def test_004_search_collection(self, content):
		"""搜索--藏品"""
		try:
			collection_button = self.driver.find_element(By.ID, "collection_radio_button")
			collection_button.click()
			self.driver.implicitly_wait(10)
			time.sleep(2)
			req = Four_Vesion_Api().searchLotPage_420(content)
			if req.json()['total'] == "0":
				is_error_toast = PublicShell(self.driver).is_elementExits(By.XPATH, "//*[contains(@text, '暂无相关藏品')]")
				assert is_error_toast == True
			else:
				resutlt = req.json()['rows']
				search_list_view = self.driver.find_element_by_id('cn.dcpai.auction:id/search_result_list_view')
				search_list_view_size = search_list_view.size
				init_hight = search_list_view.location['y']  # 结果列表页左上方高度
				results_list_view = search_list_view.find_elements_by_class_name('android.widget.LinearLayout')
				one_view_size = results_list_view[0].size  # 每个结果的尺寸大小
				show_num = search_list_view_size['height'] / one_view_size['height']  # 每页可见数量
				show_num = round(show_num)  # 可见列数(采用四舍五入的方式。因为显示不全可能会导致无法读取数据)
				cycle_index = int(len(resutlt) / show_num)
				for i in range(cycle_index):
					for j in range(show_num):
						lot_name = results_list_view[j].find_element(By.XPATH,
																	   "//*[contains(@resource-id,'search_result_lot_name')]").text
						api_lot_name = resutlt[i * show_num + j]['name']
						assert lot_name == api_lot_name, u"藏品名字展示和接口返回一致"
						lot_begin_price = results_list_view[j].find_element(By.XPATH,
																		"//*[contains(@resource-id,'search_result_lot_price')]").text
						api_lot_begin_price = resutlt[i * show_num + j]['beginPrice']
						assert float(api_lot_begin_price) ==  float(''.join(re.findall('[0-9]', lot_begin_price))), u"藏品起拍价展示和接口返回一致"
						lot_marketPriceValue = results_list_view[j].find_element(By.XPATH,
																			"//*[contains(@resource-id,'search_evaluation_price')]").text
						lot_marketPriceValue = lot_marketPriceValue[5:]			# 去掉市场估价:
						api_lot_marketPriceValue = resutlt[i * show_num + j]['marketPriceValue']
						assert lot_marketPriceValue == api_lot_marketPriceValue, u"市场估价一致"
					self.driver.swipe \
						(results_list_view[show_num - 1].location["x"],
						 results_list_view[show_num - 1].location["y"] + one_view_size['height'],
						 results_list_view[show_num - 1].location["x"], init_hight, duration=4000)
					self.driver.implicitly_wait(10)
					time.sleep(4)
		except Exception as e:
			raise e

if __name__ == '__main__':
	pytest.main("-m")
