#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/28 10:02'

"""
缴纳保证金界面
"""

import os,sys
import time
import re,random
from Command.command import command as cmd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from API.Order500 import *
from API.new_500 import *
from adblogcat.logcat import *
from adb_command.adb import *

class PayMargin:

    # 界面初始信息验证
    def Assert_INIT(self, driver, auctionId):
        try:
            ARQ = v5().findAuctionDetail(auctionId)
            BIDPRICE = float(ARQ.json()['minBidBondAmount'])
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.BidBondPaymentNewActivity'
            Title = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text,'缴纳保证金')]")))
            PayButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text,'立即支付')]")))
            # 保证金总金额
            BidText = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "nonspecially_lot_bond_amount")))
            Total = float(''.join(re.findall('\d', str(BidText.text).replace(',',''))))
            assert Total == BIDPRICE
            # 可用余额焦点控件图
            OriginCanUseMoney = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_balance_CheckBox")))
            RQ = V5_ORDER().getAccountInfo_230()
            CanUseMoney = RQ.json()['balanceAccount']['canUseAmount']   # 可用余额
            AlreadMoney = RQ.json()['bidBondAccount']['balance']        # 保证金账户总额
            if float(CanUseMoney) > 0:
                assert OriginCanUseMoney.get_attribute('enabled') == 'true'
                if OriginCanUseMoney.get_attribute('checked') =='false':
                    OriginCanUseMoney.click()
            else:
                assert OriginCanUseMoney.get_attribute('enabled') == 'false'
            # 可用余额
            CanPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_use_member_balance_money")))
            CanPayMoney = float(''.join(re.findall('\d', str(CanPay.text).replace(',',''))))
            # 待支付金额
            NeedPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_need_pay_money")))
            NeedPayMoney = float(''.join(re.findall('\d', str(NeedPay.text).replace(',',''))))
            # 已缴纳的保证金
            AlreadPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_already_pay_amount")))
            AlreadPayMoney = float(''.join(re.findall('\d', str(AlreadPay.text).replace(',',''))))
            assert AlreadPayMoney == float(AlreadMoney)
            assert NeedPayMoney == float(Total) - CanPayMoney
        except:
            assert True == False

    # 支付方式验证
    def PayMethod(self, driver):
        try:
            PayButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "immediately_payment_btn")))
            assert PayButton.text == '立即支付'
            PayButton.click()
            time.sleep(1)
            driver.implicitly_wait(5)
            WXPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "weixin_payment_type_check")))
            ZFBPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "zhifubao_payment_type_check")))
            OFFLINEPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "offline_payment_type_check")))
            SUREPAY = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "bid_bond_confirm_pay_btn")))
            if WXPay.get_attribute('checked') =='true':
                pass
            else:
                WXPay.click()
            SUREPAY.click()
            time.sleep(2)
            # 已安装微信
            if 'package:com.tencent.mm' in ADB().getList():
                assert current_package() == 'com.tencent.mm'
                driver.back()
                time.sleep(2)
            else:
                assert current_package() == 'cn.dcpai.auction'
            # 支付宝支付
            PayButton.click()
            time.sleep(1)
            if ZFBPay.get_attribute('checked') == 'true':
                pass
            else:
                ZFBPay.click()
            SUREPAY.click()
            time.sleep(2)
            assert driver.current_activity == 'com.alipay.sdk.app.H5PayActivity'
            driver.back()
            time.sleep(2)
            PayButton.click()
            time.sleep(1)
            if OFFLINEPay.get_attribute('checked') == 'true':
                pass
            else:
                OFFLINEPay.click()
            SUREPAY.click()
            driver.implicitly_wait(1)
            try:
                WebDriverWait(driver, timeout=3).until\
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "线下支付保证金")]')))
                assert driver.current_activity == '.activity.WebViewActivity'
                driver.back()
            except:
                assert True == False
        except:
            assert True == False

    # 秒啪拍场支付信息
    def DelayAuction_INIT(self, driver, auctionId):
        try:
            ARQ = v5().findDelayAucAuctionDetail_420(auctionId)
            BIDPRICE = float(ARQ.json()['minBidBondAmount'])
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.BidBondPaymentNewActivity'
            Title = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text,'缴纳保证金')]")))
            PayButton = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[contains(@text,'立即支付')]")))
            # 保证金总金额
            BidText = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "nonspecially_lot_bond_amount")))
            Total = float(''.join(re.findall('\d', str(BidText.text).replace(',',''))))
            assert Total == BIDPRICE
            # 可用余额焦点控件图
            OriginCanUseMoney = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_balance_CheckBox")))
            RQ = V5_ORDER().getAccountInfo_230()
            CanUseMoney = RQ.json()['balanceAccount']['canUseAmount']   # 可用余额
            AlreadMoney = RQ.json()['bidBondAccount']['balance']        # 保证金账户总额
            if float(CanUseMoney) > 0:
                assert OriginCanUseMoney.get_attribute('enabled') == 'true'
                if OriginCanUseMoney.get_attribute('checked') =='false':
                    OriginCanUseMoney.click()
            else:
                assert OriginCanUseMoney.get_attribute('enabled') == 'false'
            # 可用余额
            CanPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_use_member_balance_money")))
            CanPayMoney = float(''.join(re.findall('\d', str(CanPay.text).replace(',',''))))
            # 待支付金额
            NeedPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_need_pay_money")))
            NeedPayMoney = float(''.join(re.findall('\d', str(NeedPay.text).replace(',',''))))
            # 已缴纳的保证金
            AlreadPay = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "non_bid_bond_already_pay_amount")))
            AlreadPayMoney = float(''.join(re.findall('\d', str(AlreadPay.text).replace(',',''))))
            assert AlreadPayMoney == float(AlreadMoney)
            assert NeedPayMoney == float(Total) - CanPayMoney
        except:
            assert True == False