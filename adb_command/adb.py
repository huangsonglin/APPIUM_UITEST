#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/1/30 14:22'



import os
import sys
import re,time
import subprocess
import datetime

class ADB:

    # 模拟器安装路径
    path = r"D:\Program Files (x86)\BluestacksCN\BluestacksGP.exe"

    # 是否链接上设备
    def connectDevices(self):
        try:
            deviceInfo = subprocess.check_output('adb devices')
            deviceInfo = (str(deviceInfo, encoding='utf-8')).split('\r\n')
            # 如果截取后二个元素为空时这当前未链接设备
            if deviceInfo[1] == '':
                return False
            else:
                return True
        except Exception as e:
            raise e

    # 获取设备信息
    def get_devicename(self):
        if self.connectDevices():
            devices = subprocess.check_output('adb devices')
            devices = str(devices, encoding='utf-8').split('\r\n')
            devicename = devices[1]
            devicename = devicename.split('\t')
            devicename = devicename[0]
            return devicename
        else:
            # 启动模拟器
            os.startfile(self.path)
            time.sleep(60)
            subprocess.Popen('adb kill-sever')
            subprocess.Popen('adb start-sever')
            self.get_devicename()

    # 获取系统版本号
    def get_system(self):
        if self.connectDevices():
            name = self.get_devicename()
            system = subprocess.check_output(f'adb -s {name} shell getprop ro.build.version.release')
            systemNo = str(system, encoding='utf-8').split('\r\r\n')[0]
            return systemNo


    # 获取应用程序列表
    def getList(self):
        if self.connectDevices() == True:
            allList = subprocess.check_output('adb shell pm list package')
            # allList = str(allList, encoding='utf-8').split('\r\n')
            allList = re.findall('package:(.*?)\r\n',str(allList, encoding='utf-8'))
            return allList

