#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2020/2/25 11:19'

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pytesseract
from PIL import Image


def cut_img(img, *location):
	if os.path.exists(img):
		Img = Image.open(img)
		Img.crop(location).save(img)


class ReadImg:

	def __init__(self, filename, threshold):
		self.img = Image.open(filename)
		self.threshold = 175

	def binarizing(self):
		"""传入image对象进行灰度、二值处理"""
		img_obj = self.img.convert("L")  # 转灰度
		pixdata = img_obj.load()
		w, h = img_obj.size
		# 遍历所有像素，大于阈值的为黑色
		for y in range(h):
			for x in range(w):
				if pixdata[x, y] < self.threshold:
					pixdata[x, y] = 0
				else:
					pixdata[x, y] = 255
		return img_obj

	def depoint(self):
		"""传入二值化后的图片进行降噪"""
		img = self.binarizing()
		pixdata = img.load()
		w, h = img.size
		for y in range(1, h - 1):
			for x in range(1, w - 1):
				count = 0
				if pixdata[x, y - 1] > 245:  # 上
					count = count + 1
				if pixdata[x, y + 1] > 245:  # 下
					count = count + 1
				if pixdata[x - 1, y] > 245:  # 左
					count = count + 1
				if pixdata[x + 1, y] > 245:  # 右
					count = count + 1
				if pixdata[x - 1, y - 1] > 245:  # 左上
					count = count + 1
				if pixdata[x - 1, y + 1] > 245:  # 左下
					count = count + 1
				if pixdata[x + 1, y - 1] > 245:  # 右上
					count = count + 1
				if pixdata[x + 1, y + 1] > 245:  # 右下
					count = count + 1
				if count > 4:
					pixdata[x, y] = 255
		return img

	def get(self, language=None):
		code_img = self.depoint()
		pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
		text = pytesseract.image_to_string(code_img, lang=language)
		code = text.replace(' ', '').replace('\n', '')
		return code


if __name__ == '__main__':
	print(ReadImg(r"D:\TestWork\UITEST\Img\code.png", 180).get())
