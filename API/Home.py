#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/9/11 15:39'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Until.YamlRead import *
from urllib import request
from urllib import parse
from urllib import error


class HOME_API:

	def __init__(self):
		self.host = Config(CONFIG_FILE).get('host')
		self.headers = Config(CONFIG_FILE).get('headers')
		self.timeout = 1

	def findExistInLive_520(self):
		"""获取首页四大金刚，是否存在直播的状态"""
		url = self.host + 'interface/mobile/pmall/findExistInLive_520'
		req = request.Request(url, headers=self.headers, method='POST')
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findBidAuctionList_520(self, page=1, rows=20):
		"""21点轰啪列表接口"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findBidAuctionList_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findDelayAuctionList_520(self, page=1, rows=10):
		"""正在秒啪列表"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findDelayAuctionList_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findExquisiteLotList_520(self):
		"""精选推荐列表接口"""
		url = self.host + 'interface/mobile/pmall/findExquisiteLotList_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findMiniReports_520(self):
		"""江湖传闻接口"""
		url = self.host + 'interface/mobile/pmall/findMiniReports_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findReportList_520(self, id, page=1, rows=10):
		"""传闻列表页面"""
		data = {"id": id, "page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findReportList_520'
		req = request.Request(url, headers=self.headers, method="POST", data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findExhibitionLiveList_520(self):
		"""巡展直播合集接口"""
		url = self.host + 'interface/mobile/pmall/findExhibitionLiveList_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findAuctionGroupList_520(self):
		"""季拍合集列表接口"""
		url = self.host + 'interface/mobile/pmall/findAuctionGroupList_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findToDayAuctionList_520(self):
		"""今日轰啪列表"""
		url = self.host + 'interface/mobile/pmall/findToDayAuctionList_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findInDelayAuction_520(self):
		"""秒啪进行时接口列表"""
		url = self.host + 'interface/mobile/pmall/findInDelayAuction_520'
		req = request.Request(url, headers=self.headers, method="POST")
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findProductListByTypes_520(self, page=1, rows=10):
		"""拍品|商品-- 全部列表"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findProductListByTypes_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findShopProductList_520(self, page=1, rows=50):
		"""拍品|商品-- 商城列表"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findShopProductList_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findBidAuctionLotList_520(self, page=1, rows=50):
		"""拍品|商品- 轰啪列表"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findBidAuctionLotList_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason

	def findDelayAuctionLotList_520(self, page=1, rows=50):
		"""拍品|商品- 秒啪列表"""
		data = {"page": page, "rows": rows}
		data = parse.urlencode(data).encode()
		url = self.host + 'interface/mobile/pmall/findDelayAuctionLotList_520'
		req = request.Request(url, headers=self.headers, data=data)
		try:
			Response = request.urlopen(req, timeout=self.timeout)
			return Response
		except error.HTTPError as e:
			return e.reason


if __name__ == '__main__':
	req = HOME_API().findBidAuctionList_520()
	print(req.read().decode("utf-8"))
