#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/1/30 14:22'
"""
主要功能是查看当前系统是否存在Android客户端，如果没有的情况就启动模拟器。
在成功启动Android后，查看当前客服端对应的系统版本号和已安装的app应用
"""
import os
import sys
import subprocess
import time

class Adb_System():

    def __init__(self):
        # 模拟器安装路径
        self.phone_path = r"D:\Program Files (x86)\BluestacksCN\BluestacksGP.exe"
        has_devices = subprocess.check_output('adb devices')
        deviceList = (str(has_devices, encoding='utf-8')).split('\r\n')
        if deviceList[1] == '':
            # os方法启动模拟器
            os.startfile(self.phone_path)
            time.sleep(30)
            subprocess.Popen("adb kill-server")
            subprocess.Popen("adb start-server")
            time.sleep(5)
        has_devices = subprocess.check_output('adb devices')
        deviceList = (str(has_devices, encoding='utf-8')).split('\r\n')
        name = deviceList[1]
        name = name.split('\t')
        self.devicename = name[0]

    # 获取系统版本号
    def get_system(self):
        system = subprocess.check_output(f'adb -s {self.devicename} shell getprop ro.build.version.release')
        systemNo = str(system, encoding='utf-8').split('\r\r\n')[0]
        return systemNo

    # 获取应用程序列表
    def getList(self):
        allList = subprocess.check_output('adb shell pm list package')
        allList = re.findall('package:(.*?)\r\n',str(allList, encoding='utf-8'))
        return allList