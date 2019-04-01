#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/7 10:11'


import os
import datetime

def GetFile(file_dir):
    Date = datetime.datetime.now().date().strftime('%Y%m%d')
    ListName = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            FileName = os.path.splitext(file)[0]
            FileHZ = os.path.splitext(file)[1]
            if Date in FileName and 'new' not in FileName and FileHZ == '.png':
                ListName.append(os.path.join(root, file))
    return ListName
