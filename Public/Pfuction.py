#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/3/5 17:04'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class PFuction:

	def num_swtich_string(self, index):
		num_dict = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
					'5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '10': '十', "11": "十一",
					"12": "十二", "13": "十三", "14": "十四", "15": "十五", "16": "十六", "17": "十七", "18": "十八", "19": "十九",
					"20": "二十", }
		return num_dict[str(index)]

	def auction_swtich_status(self, status):
		if status == "F":
			return "已结束"
		elif status == "A":
			return "拍卖中"
		elif status == "S":
			return "暂停中"
		else:
			return "未开始"
