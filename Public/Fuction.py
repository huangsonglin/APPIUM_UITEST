#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/12/18 19:18'

import os
import sys
import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from command.driver_command import PublicShell
from adb_command.adb import Adb_System

"""
常用操作
"""
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Public_Function:

	# 从主页退出登录
	def quit_login(self, driver):
		element_user_bar = driver.find_element_by_id('rl_user_bar')  # 用户信息条
		element_user_bar.click()
		time.sleep(0.5)
		PublicShell(driver).up_swipe()
		assert '.activity.MyInfoActivity' == driver.current_activity, u"我的资料界面activity正常"
		logout = driver.find_element_by_id('cn.dcpai.auction:id/btn_logout')
		logout.click()
		time.sleep(1)

	# 进入账号登录页面
	def into_login_page(self, driver):
		if driver.current_activity == '.activity.LoginMainActivity':
			user_login = driver.find_element_by_id('btn_mobile_login')
			user_login.click()
		elif driver.current_activity == '.MainActivity':
			ele = driver.find_element(By.ID, 'cn.dcpai.auction:id/mine')
			ele.click()
			driver.implicitly_wait(1)
			time.sleep(5)
			if driver.current_activity == ".MainActivity":
				user_bar = driver.find_element_by_id('cn.dcpai.auction:id/rl_user_bar')
				user_bar.click()
				time.sleep(5)
				driver.implicitly_wait(1)
				PublicShell(driver).up_swipe()
				logout = driver.find_element_by_id('cn.dcpai.auction:id/btn_logout')
				logout.click()
				driver.implicitly_wait(0.5)
			self.into_login_page(driver)
		else:
			exit(1)

	# 账号信息登录
	def user_login(self, driver, username, password):
		self.into_login_page(driver)
		phone = WebDriverWait(driver, timeout=1).until(
			EC.visibility_of_element_located((By.ID, "et_mobile")), message="登录手机号码")
		pwd = WebDriverWait(driver, timeout=1).until(
			EC.visibility_of_element_located((By.ID, "et_password")), message="登录密码")
		login = WebDriverWait(driver, timeout=1).until(
			EC.visibility_of_element_located((By.ID, "btn_login")), message="登录按钮")
		phone.clear()
		phone.send_keys(username)
		pwd.clear()
		pwd.send_keys(password)
		login.click()

	# 进入用户中心页面
	def into_personal_center(self, driver):
		try:
			ele = driver.find_element(By.ID, 'cn.dcpai.auction:id/mine')
			ele.click()
		except Exception as e:
			raise e

	def is_emulator(self):
		"""判断是否是模拟器"""
		name = Adb_System().devicename
		if "emulator" in name:
			return True
		else:
			return False

	# 随机名字
	def random_name(self, num):
		varchar = ''
		if str(num).isdigit():
			for i in range(int(num)):
				Text = chr(random.randint(0x4e00, 0x4e20))
				varchar += Text
		return varchar


if __name__ == '__main__':
    Public_Function().random_name(1)