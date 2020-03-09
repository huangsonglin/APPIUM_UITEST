#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/3/5 14:21'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Driver.driver import AndroidDriver
import time
import json
import re
from Until.YamlRead import *
from command.driver_command import PublicShell
from Public.Fuction import Public_Function
from API.Home import HOME_API
from Public.Pfuction import PFuction


class Test_Home_BidAuction():

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

	def test_001_init(self):
		"""初始状态信息"""
		try:
			enter_auction_element = self.driver.find_element_by_android_uiautomator \
				('new UiSelector().resourceId("cn.dcpai.auction:id/home_auction").text("21点轰啪")')
			enter_auction_element.click()
			self.driver.implicitly_wait(10)
			time.sleep(0.5)
			assert self.driver.current_activity == ".frame.home.BidAuctionListActivity", u"跳转页面后activity和开发设置的一样"
			assert self.driver.find_element_by_id("title_txt").text == "21点轰啪"
		except Exception as e:
			raise e

	def test_002_result_list(self):
		"""列表--前50个结果验证"""
		try:
			time.sleep(1)
			req = HOME_API().findBidAuctionList_520(page=1, rows=20)
			api_result = json.loads(req.read().decode("utf-8"))['rows']
			for i in range(20):
				one_auction = self.driver.find_element(By.XPATH, "//*[contains(@resource-id, 'bid_list_rv')]/*")
				className = one_auction.get_attribute("className")
				elc = one_auction.location
				esize = one_auction.size
				# 合集
				if className == "android.widget.RelativeLayout":
					assert api_result[i]['auctionGroup'] == True
					assert PublicShell(self.driver).is_elementExits(By.ID, "quarter_bg_img") == True, u"集合背景图片存在"
					# 当前选中的拍场
					select_auction = one_auction.find_element_by_id("num_item_select_tv")
					right_auction_status = one_auction.find_element_by_id("quarter_state")  # 右上角拍场状态
					left_auction_status = one_auction.find_element_by_id("quarter_timer")  # 左下角拍场状态
					auction_obser = one_auction.find_element_by_id("quarter_num")  # 围观数
					auction_num_list = one_auction.find_elements(By.XPATH,
																 "//*[contains(@resource-id, 'quarter_num_rv')]/*")
					acution_status_list = []
					for auction in api_result[i]['auctions']:
						acution_status_list.append(auction['auctionState'])
					assert len(auction_num_list) == len(auction_num_list)
					if set(acution_status_list) == {'F'}:  # 拍场全部结束
						assert select_auction.text == "第一场"
						assert right_auction_status.text == "已结束"
						assert ''.join(re.findall('[0-9]', auction_obser.text)) == api_result[i]['auctions'][0][
							'observerCount']
					elif "F" in acution_status_list:  # 有部分结束
						index = acution_status_list.count('F')
						assert select_auction.text == f"第{PFuction().num_swtich_string(index+1)}场"
						if acution_status_list[index] == "S":
							assert right_auction_status.text == "暂停中"
						elif acution_status_list[index] == "A":
							assert right_auction_status.text == "拍卖中"
						else:
							assert right_auction_status.text == "未开始"
						assert ''.join(re.findall('[0-9]', auction_obser.text)) == api_result[i]['auctions'][index][
							'observerCount']
					else:  # 全部都没结束
						assert select_auction.text == "第一场"
						if acution_status_list[0] == "S":
							assert right_auction_status.text == "暂停中"
						elif acution_status_list[0] == "A":
							assert right_auction_status.text == "拍卖中"
						else:
							assert right_auction_status.text == "未开始"
						assert ''.join(re.findall('[0-9]', auction_obser.text)) == api_result[i]['auctions'][0][
							'observerCount'], u"围观次数一致"
					auction_lot_img = one_auction.find_elements(By.ID, "lot_imageView")
					auction_num_list[0].click()
					regin_auction_num_list = one_auction.find_elements(By.XPATH,
																 "//*[contains(@resource-id, 'quarter_num_rv')]/*")
					for auction_num in regin_auction_num_list:
						auction_img = one_auction.find_element(By.ID, "quarter_img")
						k = regin_auction_num_list.index(auction_num)
						auction_num.click()
						self.driver.implicitly_wait(10)
						time.sleep(0.5)
						new_right_auction_status = self.driver.find_element(By.ID, "quarter_state")
						if acution_status_list[k] == "F":
							assert new_right_auction_status.text == "已结束"
							auction_total_price = one_auction.find_element(By.ID, "quarter_tv_price")
							auction_total_num = one_auction.find_element(By.ID, "quarter_tv_num")
							hammerPriceTotal = api_result[i]["auctions"][k]['hammerPriceTotal']
							biddingPriceCount = api_result[i]["auctions"][k]['biddingPriceCount']
							dispaly_hammerPriceTotal = ''.join(re.findall('[0-9]', auction_total_price.text))
							dispaly_biddingPriceCount = ''.join(re.findall('[0-9]', auction_total_num.text))
							assert float(dispaly_hammerPriceTotal) == float(hammerPriceTotal), u'已结束的拍场成交总价一致'
							assert dispaly_biddingPriceCount == biddingPriceCount, u'已结束的拍场成交次数一致'
							assert one_auction.find_element(By.XPATH, "//*[@text='• 成交额 •']").is_displayed() == True
						elif acution_status_list[k] == "A":
							assert new_right_auction_status.text == "进行中"
						elif acution_status_list[k] == "S":
							assert new_right_auction_status.text == "暂停中"
						else:
							assert new_right_auction_status.text == "未开始"
						new_auction_obser = self.driver.find_element_by_id("quarter_num")  # 围观数
						assert ''.join(re.findall('[0-9]', new_auction_obser.text)) == api_result[i]['auctions'][k][
							'observerCount'], u"围观次数一致"
						auction_img.click()
						self.driver.implicitly_wait(10)
						time.sleep(0.5)
						assert self.driver.current_activity == '.activity.AuctionGroupDetailNewActivity'
						group_every_api_aution_name = api_result[i]["auctions"][k]['name']
						detaile_auction_name = self.driver.find_element(By.ID, "title_title_text_view").text
						assert detaile_auction_name[0:-3] in group_every_api_aution_name
						self.driver.back()
						time.sleep(0.5)
						self.driver.implicitly_wait(10)
				else:	# 非合集
					aution_name = one_auction.find_element(By.ID, "bid_name_tv").text
					aution_status = one_auction.find_element(By.ID, "bid_state_tv").text
					aution_observerCount = ''.join(re.findall('[0-9]', one_auction.find_element(By.ID, "bid_num_tv").text))
					api_auction_status = api_result[i]['auctionState']
					api_auction_name = api_result[i]['name']
					api_auction_observerCount = api_result[i]['observerCount']
					assert aution_name == api_auction_name
					api_auction_status_text = PFuction().auction_swtich_status(api_auction_status)
					assert aution_status == api_auction_status_text
					assert aution_observerCount == api_auction_observerCount
					if api_auction_status != "F":
						# 直播拍场标签
						if 'liveStart' in list(api_result[i].keys()) and 'liveState' in list(api_result[i].keys()):
							auction_live_status = one_auction.find_element(By.ID, "bid_live_iocn_tv")
							assert auction_live_status.text == '直播'
						assert one_auction.find_element(By.ID, "bid_state_auction_tv").is_enabled() == True, u"时间"
					else:
						assert one_auction.find_element(By.XPATH, "//*[@text='• 成交额 •']").is_displayed() == True
						biddingPriceCount = api_result[i]['biddingPriceCount']
						hammerPriceTotal = api_result[i]['hammerPriceTotal']
						assert biddingPriceCount == ''.join(re.findall('[0-9]', one_auction.find_element(By.ID, "bid_tv_num").text))
						assert float(hammerPriceTotal) == float(''.join(re.findall('[0-9]', one_auction.find_element(By.ID, "bid_tv_price").text)))
					switch_button = one_auction.find_element(By.ID, "bid_switch_img")
					assert switch_button.is_enabled() == True, u"宫格列表切换"
					assert switch_button.get_attribute('clickable') == 'true'
					switch_button.click()
					self.driver.implicitly_wait(10)
					time.sleep(0.5)
					lot_img = one_auction.find_elements(By.ID, "bid_item_img")		# 拍品列表信息
					switch_button.click()
					self.driver.implicitly_wait(10)
					time.sleep(0.5)
					auction_img = one_auction.find_element(By.ID, "bid_img")  # 拍场封面信息
					auction_img.click()
					assert self.driver.current_activity == '.activity.AuctionGroupDetailNewActivity'
					detaile_auction_name = self.driver.find_element(By.ID, "title_title_text_view").text
					assert detaile_auction_name[0:-3] in api_auction_name
					self.driver.back()
					self.driver.implicitly_wait(10)
				self.driver.swipe(int(elc['x']+esize['width'])/2, elc['y']+ esize['height']+10, int(elc['x']+esize['width'])/2, elc['y']-5, duration=4000)
				self.driver.implicitly_wait(10)
				time.sleep(3)
		except Exception as e:
			raise e


if __name__ == '__main__':
	pytest.main('-m')
