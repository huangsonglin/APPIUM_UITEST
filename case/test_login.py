#!user/bin/python
# -*-coding:utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/2/25 09:59'
"""
登录测试
"""

import sys, os
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
import pytest
from adblogcat.logcat import *
from Until.DB import Mysql
from Until.YamlRead import *
from command.driver_command import PublicShell
from Until.ReadImage import *

class Test_Login():

	def setup_module(self):
		pass

	@classmethod
	def setup_class(cls):
		cls.driver = AndroidDriver().driver
		cls.name = datetime.datetime.now().strftime('%m%d')
		cls.logpath = f'{Logcat}\%s.txt' % cls.name
		cls.IMG_PATH = Base_path + r'\Img'
		cls.host = Config(CONFIG_FILE).get("host")

	@classmethod
	def teardown_class(cls):
		cls.driver.quit()

	def teardown_module(self):
		pass

	# 进入登录界面
	def test_001_into_login(self):
		"""进入登录界面"""
		ele = self.driver.find_element(By.ID, 'cn.dcpai.auction:id/mine')	# 按钮--我的
		ele.click()
		time.sleep(0.5)
		current_activity = self.driver.current_activity
		assert current_activity in [".activity.LoginMainActivity", ".MainActivity"]		# 点击我的后进入的界面只能在对应的activity中
		try:
			if current_activity == '.activity.LoginMainActivity':
				weixin_login_button = self.driver.find_element_by_id('btn_weixin_login')	# 微信登录按钮
				user_login_button = self.driver.find_element_by_id('btn_mobile_login')	 	# 账号登录按钮
				new_user_register = self.driver.find_element_by_id('tv_user_reg')			# 新用户注册
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='快速登录']") == True	# 文字-快速登陆存在

			else:
				user_icon = self.driver.find_element_by_id('iv_avatar')						# 用户头像
				user_nickname = self.driver.find_element_by_id('tv_nickname')				# 用户昵称
				user_num = self.driver.find_element_by_id('tv_account')						# 用户龖藏号
				while True:
					get_log()
					user_icon.click()
					self.driver.back()
					break
				pidList = Config(Pid_PATH).get('Pid')
				for pid in pidList:
					end_log(pid)
				with open(self.logpath, 'r', errors='ignore') as f:
					for line in f.readlines():
						if 'http://train-h5.dcpai.cn/app/interface/mobile/getMemberDetailInfo_112  response is' in line:
							memberId = re.findall('"id":"(.*?)",', line)
							break
				user_info = Mysql().sql_result(f'select name, zang_num from user where id={memberId[0]}')
				assert user_nickname.text == user_info[0][0], u"用户昵称显示一致"
				assert user_num.text.split(":")[1].strip() == user_info[0][1], u"龖藏号一致"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='我的订单']") == True, u"我的订单元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_obligation") == True, u"我的订单-待付款元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_wait_send_out") == True, u"我的订单-待发货元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_wait_take") == True, u"我的订单-待收货元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_wait_comment") == True, u"我的订单-待评价元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "tv_aftermarket") == True, u"我的订单-退款|售后元素存在"
				assert PublicShell(self.driver).is_elementExits(By.ID, "mine_msg") == True, u"消息按钮存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='我的钱包']") == True, u"我的钱包元素存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='可用余额']") == True, u"我的钱包--可用余额元素存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='待入账']") == True, u"我的钱包--待入账元素存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='保证金']") == True, u"我的钱包--保证金元素存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='龙珠']") == True, u"我的钱包--龙珠元素存在"
				assert PublicShell(self.driver).is_elementExits(By.XPATH, "//*[@text='提现']") == True, u"我的钱包--提现元素存在"
				element_user_bar = self.driver.find_element_by_id('rl_user_bar')		# 用户信息条
				element_user_bar.click()
				time.sleep(0.5)
				PublicShell(self.driver).up_swipe()
				assert '.activity.MyInfoActivity' == self.driver.current_activity, u"我的资料界面activity正常"
				logout = self.driver.find_element_by_id('cn.dcpai.auction:id/btn_logout')
				logout.click()
				time.sleep(1)
				self.test_001_into_login()
		except Exception as e:
			raise e

	# 账户和密码为空登录
	def test_002_Empty_login(self):
		"""账户和密码为空登录"""
		try:
			user_login_button = self.driver.find_element_by_id('btn_mobile_login')  # 账号登录按钮
			user_login_button.click()
			self.driver.implicitly_wait(3)
			assert self.driver.current_activity == ".activity.MobileLoginActivity", u'跳转登录界面正常'
			phone = self.driver.find_element(By.ID, "et_mobile")	# "登录手机号码"
			pwd = self.driver.find_element(By.ID, "et_password")  	# message="登录密码"
			login = self.driver.find_element(By.ID, "btn_login")	#"登录按钮"
			# 直接点击登录按钮
			login.click()
			# 无法获取toast信息,需要1.6.3以上版本方可获取提示信息
			# null_toast = WebDriverWait(self.driver, 10, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[@text='手机号不能为空']")))
			assert self.driver.current_activity == ".activity.MobileLoginActivity", u"未输入任何消息直接登录，仍停留在登录界面"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_mobile") == True, u"登录手机号码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_password") == True, u"登录密码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "btn_login") == True, u"登录按钮元素依然存在"
		except Exception as e:
			raise e

	@pytest.mark.parametrize('username_01, password_01, username_02, password_02',
							 [("3999999000a", '123456', "3999999000", '1234567')])
	def test_003_errorInfo_login(self, username_01, password_01, username_02, password_02):
		"""异常账号登录"""
		try:
			phone = WebDriverWait(self.driver, 10, 0.5).until(
				EC.visibility_of_element_located((By.ID, "et_mobile")), message="登录手机号码")
			pwd = WebDriverWait(self.driver, 10, 0.5).until(
				EC.visibility_of_element_located((By.ID, "et_password")), message="登录密码")
			login = WebDriverWait(self.driver, 10, 0.5).until(
				EC.visibility_of_element_located((By.ID, "btn_login")), message="登录按钮")
			phone.clear()
			pwd.clear()
			phone.send_keys(username_01)
			pwd.send_keys(password_01)
			login.click()
			self.driver.implicitly_wait(0.5)
			assert self.driver.current_activity == ".activity.MobileLoginActivity"
			# null_toast = WebDriverWait(self.driver, 10, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[@text='手机号不能为空']")))
			assert self.driver.current_activity == ".activity.MobileLoginActivity", u"未输入任何消息直接登录，仍停留在登录界面"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_mobile") == True, u"登录手机号码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_password") == True, u"登录密码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "btn_login") == True, u"登录按钮元素依然存在"
			phone.clear()
			pwd.clear()
			phone.send_keys(username_02)
			pwd.send_keys(password_02)
			login.click()
			self.driver.implicitly_wait(0.5)
			assert self.driver.current_activity == ".activity.MobileLoginActivity"
			# null_toast = WebDriverWait(self.driver, 10, 0.1).until(EC.presence_of_element_located((By.XPATH, "//*[@text='手机号不能为空']")))
			assert self.driver.current_activity == ".activity.MobileLoginActivity", u"未输入任何消息直接登录，仍停留在登录界面"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_mobile") == True, u"登录手机号码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "et_password") == True, u"登录密码元素依然存在"
			assert PublicShell(self.driver).is_elementExits(By.ID, "btn_login") == True, u"登录按钮元素依然存在"
		except Exception as e:
			raise e

	# 三次输错帐号信息或密码后验证码显示
	@pytest.mark.parametrize("username, password", [('39999990000', "1234567")])
	def test_004_threeError_securityCode_login(self, username, password):
		"""三次输错帐号信息或密码后验证码显示"""
		try:
			phone = WebDriverWait(self.driver, timeout=1).until(
				EC.visibility_of_element_located((By.ID, "et_mobile")), message="登录手机号码")
			pwd = WebDriverWait(self.driver, timeout=1).until(
				EC.visibility_of_element_located((By.ID, "et_password")), message="登录密码")
			login = WebDriverWait(self.driver, timeout=1).until(
				EC.visibility_of_element_located((By.ID, "btn_login")), message="登录按钮")
			phone.clear()
			pwd.clear()
			phone.send_keys(username)
			pwd.send_keys(password)
			[login.click() for i in range(2)]
			time.sleep(1)
			code = WebDriverWait(self.driver, timeout=1).until(
				EC.visibility_of_element_located((By.ID, "btn_get_code")), message="验证码")
		except Exception as e:
			raise e

	@pytest.mark.parametrize("username, password", [('39999990000', "123456")])
	def test_005_right_login(self, username, password):
		"""正常登录"""
		try:
			phone = WebDriverWait(self.driver, timeout=5).until(
				EC.visibility_of_element_located((By.ID, "et_mobile")), message="登录手机号码")
			pwd = WebDriverWait(self.driver, timeout=5).until(
				EC.visibility_of_element_located((By.ID, "et_password")), message="登录密码")
			login = WebDriverWait(self.driver, timeout=5).until(
				EC.visibility_of_element_located((By.XPATH, "//*[@class='android.widget.Button'][@text='登录']")), message="登录按钮")
			is_code = PublicShell(self.driver).is_elementExits(By.ID, "auth_code_input")
			if is_code:
				code = WebDriverWait(self.driver, timeout=5).until(
					EC.visibility_of_element_located((By.ID, "btn_get_code")), message="验证码")
				code_input = self.driver.find_element(By.ID, "auth_code_input")
				img_name = os.path.join(self.IMG_PATH, "code.png")
				self.driver.save_screenshot(img_name)
				cut_img(img_name, code.location['x'], code.location['y'],
						code.location['x'] + code.size['width'], code.location['y'] + code.size['height'])
				code_text = ReadImg(img_name, 175).get()
				# 因为技术不成熟导致需要多次刷新验证码，直到能够识别出来方可
				while True:
					# 读取出来的code码长度为4且只能是数字和字母组成
					if len(code_text) == 4 and code_text.isalnum():
						break
					else:
						code.click()
						self.driver.implicitly_wait(1)
						self.driver.save_screenshot(img_name)
						cut_img(img_name, code.location['x'], code.location['y'],
								code.location['x'] + code.size['width'], code.location['y'] + code.size['height'])
						code_text = ReadImg(img_name, 175).get()
				code_input.clear()
				code_input.send_keys(code_text)
			get_log()
			phone.send_keys(username)
			pwd.send_keys(password)
			self.driver.implicitly_wait(1)
			login.click()
			time.sleep(0.2)
			pidList = Config(Pid_PATH).get('Pid')
			for pid in pidList:
				end_log(pid)
			assert self.driver.current_activity == ".MainActivity", u"已登录情况下当前为MainActivity"
			user_icon = self.driver.find_element_by_id('iv_avatar')
			user_nickname = self.driver.find_element_by_id('tv_nickname')
			user_num = self.driver.find_element_by_id('tv_account')
			with open(self.logpath, 'r', errors='ignore') as f:
				for line in f.readlines():
					if self.host+'interface/mobile/pmall/loginByPhone_220  response is' in line:
						memberId = re.findall('"id":"(.*?)",', line)
						break
			user_info = Mysql().sql_result(f'select name, zang_num from user where id={memberId[0]}')
			assert user_nickname.text == user_info[0][0]
			assert user_num.text.split(":")[1].strip() == user_info[0][1]
		except Exception as e:
			raise e
