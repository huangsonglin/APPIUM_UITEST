#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/19 18:00'

import subprocess
import datetime
import os,re
import time
import json
from Until.YamlRead import *
from adb_command.adb import Adb_System

global BTest
BTest = None

def get_log():
    devicename = Adb_System().devicename
    tasklist = 'tasklist | findstr "adb"'
    AdbList1 = os.popen(tasklist)
    beforeText = (AdbList1.read().replace(' ', '').replace('\n', ''))
    beforPid = re.findall('exe(.*?)Console', beforeText)
    name = datetime.datetime.now().strftime('%m%d')
    logpath = f'{Logcat}\%s.txt' % name
    with open(logpath, 'w', encoding='utf-8') as f:
        order = f'adb -s {devicename} logcat find "cn.dcpai.auction" >{logpath}'  # 获取连接设备
        pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    tasklist = 'tasklist | findstr "adb"'
    AdbList2 = os.popen(tasklist)
    afterText = (AdbList2.read().replace(' ', '').replace('\n', ''))
    afterPid = re.findall('exe(.*?)Console', afterText)
    LogPid = {}
    pids = []
    for pid in afterPid:
        if pid not in beforPid:
            pids.append(pid)
    LogPid.update(Pid=pids)
    yaml_write(Pid_PATH).write(LogPid)

def end_log(pid):
    end = subprocess.Popen('taskkill /f /t /pid %s' % pid, shell=True)


# 获取调用登录接口后的token信息
def get_Login_token():
    name = datetime.datetime.now().strftime('%m%d')
    file = f'{Logcat}\%s.txt' % name
    if os.path.exists(file):
        file = open(file, encoding='utf-8', errors='ignore')
        for readline in file.readlines():
            if 'http://testapp.dcpai.cn/app/interface/mobile/pmall/loginByPhone_220  response is' in readline:
                data = re.findall('response is (.*)', readline)[0]
                data = json.loads(data)
                token = 'Bearer ' + data['accessToken']
                yaml_write(App_LoginToken).write({'Authorization': token})
                break

# 获取已登录的token信息
def get_Token():
    name = datetime.datetime.now().strftime('%m%d')
    file = f'{Logcat}\%s.txt' % name
    if os.path.exists(file):
        file = open(file, encoding="utf-8", errors='ignore')
        for readline in file.readlines():
            if 'Authorization' in readline:
                Authorization = re.findall('Authorization: (.*)', readline)[0]
                yaml_write(App_LoginToken).write({'Authorization': Authorization})
                break

# 获取当前设备信息显示界面的包名
def current_package():
    devicename = Adb_System().devicename
    cmd = f'adb -s {devicename} shell dumpsys window w |findstr \/ |findstr name='
    pakgeList = os.popen(cmd).read()
    pakge = re.findall('name=(.*?)/', pakgeList)[0]
    return pakge


