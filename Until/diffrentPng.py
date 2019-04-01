#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/6 17:00'

"""
比较两张图片是否相同
"""

from PIL import Image
from PIL import ImageChops
from Until.YamlRead import *
import os


def CompareImg(One_Image, Two_Image, box):
    """
    :param One_Image:  第一张图片的详细路径
    :param Two_Image:  第一张图片的详细路径
    :param box:        要截取的位置（start_x, start_y, end_x, end_y）
    :return:           一致则True，反之False
    """
    image_one = Image.open(One_Image)
    image_two = Image.open(Two_Image)
    newOne = image_one.crop(box)
    One_Image_Name = os.path.split(One_Image)[1]
    Two_Image_Name = os.path.split(Two_Image)[1]
    newonepath = IMG_PATH + u'\\new_%s' % One_Image_Name
    newOne.save(newonepath)
    newTwo = image_two.crop(box)
    newtwopath = IMG_PATH + u'\\new_%s' % Two_Image_Name
    newTwo.save(newtwopath)
    new_image_one = Image.open(newonepath)
    new_image_two = Image.open(newtwopath)
    try:
        diff = ImageChops.difference(image_one, image_two)
        if diff.getbbox() is None:
            return True
        else:
            return False
    except ValueError as e:
       raise e

def CompareImg1(One_Image, Two_Image):
    image_one = Image.open(One_Image)
    image_two = Image.open(Two_Image)
    try:
        diff = ImageChops.difference(image_one, image_two)
        if diff.getbbox() is None:
            return True
        else:
            return False
    except ValueError as e:
       raise e

