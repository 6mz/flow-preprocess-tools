# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 21:10:58 2019

@author: Administrator
"""

import mynumpy as m
import numpy as np
from PIL import Image
from datasets_lib1 import Point, Rect, RectArray, Obj, Trans, Board
import datasets_func as func

import cv2

def DisplayObject(obj):
    imArray = obj.data * obj.dataMask + obj.data * 0.2
    imArray = imArray / np.max(imArray) * 255
    imArray = np.uint8(imArray)
    im = Image.fromarray(imArray)
    im.show()


im = np.array(Image.open('../data/ds_v1/timg.jpg'))

pos = func.RandomPoint([-100, -100], [300, 300])
# size = func.RandomSize([10, 10], [50, 50])
size = im.shape[0:2]

obj1_rect = Rect(pos, size)
obj1_data = RectArray(obj1_rect, 3)
obj1_data.SetRectData(im)

immask = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)<240
#Image.fromarray(np.uint8(immask*255)).show()

obj1_datamask = RectArray(obj1_rect, 1, dtype=np.bool)
obj1_datamask.SetValue(immask)
#
#obj1_mask_rect = Rect(Point(75, 75), size2)
#obj1_true_datamask = RectArray(obj1_mask_rect, 1, dtype=np.bool)
#obj1_true_datamask.SetValue(False)
#
#obj1_datamask.AddRectArray(obj1_true_datamask, CSYS='local')
#
#
obj1 = Obj(obj1_data, obj1_datamask)
trans = Trans(obj1)
#pts = trans.GenTrans('py')
pts = trans.GenTrans('xz')
trans.ImposeTrans(pts)
#DisplayObject(obj1)
mainboard = Board([1000, 1000])
mainboard.addTrans(trans)
mainboard.Gen()
mainboard.Display('imA')
mainboard.Display('imB')
look = mainboard.Display('flowA')
#print(obj1)
#look = obj1.data_
#look2 = obj1.dataMask_
