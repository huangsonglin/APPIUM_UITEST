#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/12/19 14:52'

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
import random
import string
from adblogcat.logcat import *
from Until.DB import Mysql
from Until.YamlRead import *
from command.driver_command import PublicShell
from Public.Fuction import Public_Function
from API.V5down import Four_Vesion_Api
import pytest


class Test_Register():

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

	# 注册页面UI验证
	def test_001_into_register_page(self):
		"""注册页面UI验证"""
		try:
			ele = self.driver.find_element(By.ID, 'cn.dcpai.auction:id/mine')  # 按钮--我的
			ele.click()
			time.sleep(0.5)
			current_activity = self.driver.current_activity
			assert current_activity in [".activity.LoginMainActivity", ".MainActivity"]  # 点击我的后进入的界面只能在对应的activity中
			# 注册按钮是否存在
			is_register = PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='新用户注册']")
			if is_register:
				element_register = self.driver.find_element_by_xpath("//*[@text='新用户注册']")
				element_register.click()
				assert self.driver.current_activity == ".activity.MobileRegActivity", u"注册界面activity正常"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='注册']") == True, u"注册title可见"
				assert PublicShell(self.driver).is_elementExits(By.ID, "et_number") == True, u"国际注册码可见"
				assert self.driver.find_element(By.ID, "et_number").get_attribute("text") == "+86", u'国际注册码默认为中国区号'
				assert PublicShell(self.driver).is_elementExits(By.ID, "et_mobile") == True, u"手机号注册框可见"
				assert self.driver.find_element(By.ID, "et_mobile").get_attribute("text") == "请输入手机号"
				assert PublicShell(self.driver).is_elementExits(By.ID, "et_code") == True, u"验证码框可见"
				assert self.driver.find_element(By.ID, "et_code").get_attribute("text") == "请输入验证码"
				assert PublicShell(self.driver).is_elementExits(By.ID, "btn_get_code") == True, u"发送验证码可见"
				assert self.driver.find_element(By.ID, "btn_get_code").get_attribute("text") == "获取验证码"
				assert PublicShell(self.driver).is_elementExits(By.ID, "et_nickname") == True, u"昵称输入框可见"
				assert self.driver.find_element(By.ID, "et_nickname").get_attribute("text") == "请输入昵称(15个字以内)"
				assert PublicShell(self.driver).is_elementExits(By.ID, "et_password") == True, u"密码输入框可见"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_text") == True, u"同意协议"
				assert self.driver.find_element(By.ID, "tv_text").get_attribute("text") == "我已阅读并同意"
				assert PublicShell(self.driver).is_elementExits(By.XPATH,
																"//*[contains(@text,'龘藏用户协议')]") == True, u"同意协议"
				assert PublicShell(self.driver).is_elementExits(By.ID, "btn_register") == True, u"注册按钮"
			else:

				# 从主页退出登录
				Public_Function().quit_login(self.driver)
				self.driver.implicitly_wait(1)
				self.test_001_into_register_page
		except Exception as e:
			raise e

	# 空内容进行注册
	def test_02_empty_content_register(self):
		"""空内容进行注册"""
		try:
			ele_commit = self.driver.find_element_by_id('btn_register')
			ele_commit.click()
			assert self.driver.current_activity == '.activity.MobileRegActivity', u"所有信息为空时注册功能正常"

		except Exception as e:
			raise e

	# 密码长度不满足要求
	def test_03_except_password_register(self):
		"""密码长度不满足要求"""
		try:
			# 已注册的号码
			all_phone = Mysql().sql_result('select username from user')
			while True:
				tel = random.randint(19800000000, 19899999999)
				if (str(tel),) not in all_phone:
					break
			ele_mobile = self.driver.find_element_by_id("et_mobile")
			ele_code = self.driver.find_element_by_id('et_code')
			ele_get_code = self.driver.find_element(By.ID, "btn_get_code")
			ele_nikename = self.driver.find_element(By.ID, "et_nickname")
			ele_password = self.driver.find_element_by_id('et_password')
			ele_commit = self.driver.find_element_by_id('btn_register')
			req = Four_Vesion_Api().sendAuthenticationCode_112(tel)
			time.sleep(0.5)
			db_code = Mysql().reslut_replace(
				f'SELECT message FROM sms_send_his WHERE phone={tel} ORDER BY id DESC LIMIT 1')
			code = re.findall('验证码是(.*)，5分钟', db_code)
			code = code[0]
			ele_mobile.clear()
			ele_mobile.send_keys(tel)
			ele_code.clear()
			ele_code.send_keys(code)
			ele_nikename.clear()
			ele_nikename.send_keys(Public_Function().random_name(3))
			ele_commit.click()
			assert self.driver.current_activity == '.activity.MobileRegActivity', u"密码为空时注册功能正常"
			sort_pwd = '12345'
			long_pwd = '12345123451234512'
			ele_password.clear()
			ele_password.send_keys(sort_pwd)
			ele_commit.click()
			long_name = Public_Function().random_name(16)
			assert self.driver.current_activity == '.activity.MobileRegActivity', u"密码长度低于6位时注册功能正常"
			ele_password.clear()
			if not Public_Function().is_emulator():
				ele_password.send_keys(long_pwd)
				ele_commit.click()
				assert self.driver.current_activity == '.activity.MobileRegActivity', u"密码长度高于16位时注册功能正常"
				ele_nikename.clear()
				ele_nikename.send_keys(long_name)
				ele_password.send_keys("123456")
				ele_commit.click()
				assert self.driver.current_activity == '.activity.MobileRegActivity', u"昵称长度高于16位时注册功能正常"
		except Exception as e:
			raise e

	# 已注册的号码重新注册
	def test_04_hasregister_again(self):
		"""已注册的号码重新注册"""
		try:
			# 已注册的号码
			all_phone = Mysql().sql_result('select username from user')
			tel = random.choice(all_phone)[0]
			ele_mobile = self.driver.find_element_by_id("et_mobile")
			ele_code = self.driver.find_element_by_id('et_code')
			ele_get_code = self.driver.find_element(By.ID, "btn_get_code")
			ele_nikename = self.driver.find_element(By.ID, "et_nickname")
			ele_password = self.driver.find_element_by_id('et_password')
			ele_commit = self.driver.find_element_by_id('btn_register')
			req = Four_Vesion_Api().sendAuthenticationCode_112(tel)
			time.sleep(0.5)
			db_code = Mysql().reslut_replace(
				f'SELECT message FROM sms_send_his WHERE phone={tel} ORDER BY id DESC LIMIT 1')
			code = re.findall('验证码是(.*)，5分钟', db_code)
			code = code[0]
			ele_mobile.clear()
			ele_mobile.send_keys(tel)
			ele_code.clear()
			ele_code.send_keys(code)
			ele_nikename.clear()
			ele_nikename.send_keys(Public_Function().random_name(3))
			pwd = '123456'
			ele_password.clear()
			ele_password.send_keys(pwd)
			ele_commit.click()
			assert self.driver.current_activity == '.activity.MobileRegActivity', u"已注册的号码再次注册功能正常"
		except Exception as e:
			raise e

	# 验证码不正确进行注册
	def test_05_errorcode_register(self):
		"""验证码不正确进行注册"""
		try:
			all_phone = Mysql().sql_result('select username from user')
			while True:
				tel = random.randint(19800000000, 19899999999)
				if (str(tel),) not in all_phone:
					break
			ele_mobile = self.driver.find_element_by_id("et_mobile")
			ele_code = self.driver.find_element_by_id('et_code')
			ele_get_code = self.driver.find_element(By.ID, "btn_get_code")
			ele_nikename = self.driver.find_element(By.ID, "et_nickname")
			ele_password = self.driver.find_element_by_id('et_password')
			ele_commit = self.driver.find_element_by_id('btn_register')
			code = ''.join(random.sample(string.digits, 6))
			ele_mobile.clear()
			ele_mobile.send_keys(tel)
			ele_code.clear()
			ele_code.send_keys(code)
			ele_nikename.clear()
			ele_nikename.send_keys(Public_Function().random_name(3))
			pwd = '123456'
			ele_password.clear()
			ele_password.send_keys(pwd)
			ele_commit.click()
			assert self.driver.current_activity == '.activity.MobileRegActivity', u"验证码正确时注册功能正常"
		except Exception as e:
			raise e

	# 正常注册
	def test_06_register(self):
		"""正常注册"""
		try:
			all_phone = Mysql().sql_result('select username from user')
			while True:
				tel = random.randint(19800000000, 19899999999)
				if (str(tel),) not in all_phone:
					break
			ele_mobile = self.driver.find_element_by_id("et_mobile")
			ele_code = self.driver.find_element_by_id('et_code')
			ele_get_code = self.driver.find_element(By.ID, "btn_get_code")
			ele_nikename = self.driver.find_element(By.ID, "et_nickname")
			ele_password = self.driver.find_element_by_id('et_password')
			ele_commit = self.driver.find_element_by_id('btn_register')
			ele_mobile.clear()
			ele_mobile.send_keys(tel)
			req = Four_Vesion_Api().sendAuthenticationCode_112(tel)
			time.sleep(0.5)
			db_code = Mysql().reslut_replace(
				f'SELECT message FROM sms_send_his WHERE phone={tel} ORDER BY id DESC LIMIT 1')
			code = re.findall('验证码是(.*)，5分钟', db_code)
			code = code[0]
			ele_code.clear()
			ele_code.send_keys(code)
			ele_password.clear()
			ele_password.send_keys('123456')
			ele_nikename.clear()
			nikename = Public_Function().random_name(3)
			ele_nikename.send_keys(nikename)
			ele_commit.click()
			assert self.driver.current_activity == '.MainActivity', u"注册成功后返回登主界面"
			user_nickname = self.driver.find_element_by_id('tv_nickname')
			assert user_nickname.text == nikename
		except Exception as e:
			raise e


if __name__ == '__main__':
	unittest.main()
