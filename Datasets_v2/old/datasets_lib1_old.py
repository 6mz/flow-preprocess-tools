# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
from PIL import Image
import cv2

import mynumpy as m


###################################################################
class Point(object):
    def __init__(self, x, y=None):
        if(isinstance(x, Point)):
            self.x = x.x
            self.y = x.y
            self.i = x.i
            self.j = x.j
        elif y is None:
            self.x = x[0]
            self.y = x[1]
            self.i = x[1]
            self.j = x[0]
        else:
            self.x = x
            self.y = y
            self.i = y
            self.j = x

    def __getitem__(self, key):
        # p[0] or p[1]
        return self.y if key else self.x

    def __add__(self, other):
        x = self.x + other[0]
        y = self.y + other[1]
        return Point(x, y)

    def __radd__(self, other):
        x = other[0] + self.x
        y = other[1] + self.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other[0]
        y = self.y - other[1]
        return np.array([x, y])

    def __rsub__(self, other):
        x = other[0] - self.x
        y = other[1] - self.y
        return np.array([x, y])

    def __mul__(self, num):
        x = self.x * num
        y = self.y * num
        return Point(x, y)

    def __str__(self):
        return ' x:%s,y:%s ' % (self.x, self.y)

    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __call__(self):
        return deepcopy(self)

###################################################################


class Rect(object):
    '''
    '''
    def __init__(self, rectPos_Or_Rect, rectSize=None):
        '''
        输入：
            rectPos_Or_Rect：二维矩形左上角坐标点/另一个矩形
            rectSize：二维矩阵的大小
        '''
        if(isinstance(rectPos_Or_Rect, Point)):
            self.rectPosPoint = rectPos_Or_Rect()
            assert(len(rectSize) == 2 and rectSize[0] > 0 and rectSize[1] > 0)
            self.rectSize = np.array(rectSize, dtype=np.int)
        elif(isinstance(rectPos_Or_Rect, Rect)):
            rect = rectPos_Or_Rect()
            self.rectPosPoint = rect.rectPosPoint
            self.rectSize = rect.rectSize

    def shape(self):
        return (self.rectSize[0], self.rectSize[1])

    def Central(self):
        # 中心点
        return Point(self.rectPosPoint + self.rectSize/2)

    def DiaCorner(self):
        # 对角点
        return Point(self.rectPosPoint + self.rectSize)

    def AllCorners(self):
        # 所有角点，顺序：
        # 12
        # 43
        corner1 = self.rectPosPoint
        corner2 = corner1 + (self.rectSize[0], 0)
        corner3 = self.diaCorner()
        corner4 = corner1 + (0, self.rectSize[1])
        return (corner1, corner2, corner3, corner4)

    def CvRect(self):
        return (np.int(self.rectPosPoint[0]), np.int(self.rectPosPoint[1]),
                np.int(self.rectSize[0]), np.int(self.rectSize[1]))

    def __str__(self):
        return ' rectPosPoint:%s,rectSize:%s ' % (
                self.rectPosPoint, self.rectSize)

    def __eq__(self, other):
        assert isinstance(other, Rect)
        return self.rectPosPoint == other.rectPosPoint and \
            (self.rectSize == other.rectSize).all()

    def __lt__(self, other):
        assert isinstance(other, Rect)
        return (self.rectSize[0] < other.rectSize[0] and
                self.rectSize[1] < other.rectSize[1])

    def __le__(self, other):
        assert isinstance(other, Rect)
        return (self.rectSize[0] <= other.rectSize[0] and
                self.rectSize[1] <= other.rectSize[1])

    def __gt__(self, other):
        assert isinstance(other, Rect)
        return (self.rectSize[0] > other.rectSize[0] and
                self.rectSize[1] > other.rectSize[1])

    def __ge__(self, other):
        assert isinstance(other, Rect)
        return (self.rectSize[0] >= other.rectSize[0] and
                self.rectSize[1] >= other.rectSize[1])

    def __call__(self):
        return deepcopy(self)

###################################################################


class RectArray(object):
    def __init__(self, rect, dim3=3, dtype=np.uint8):
        '''
        输入：
            rect：二维的Rect对象，表明RectArray的位置和大小。
            dim3：RectArray的第三维度大小，一般1为模板，2为光流，3为RGB图像。
            dtype：RectArray的数据类型，一般np.bool为模板，np.float为光流，
                np.uint8为RGB图像。
        '''
        assert(isinstance(rect, Rect))
        self.rectData = m.zeros3(rect.shape(), dim3, dtype)
        self.dtype = dtype
        self.rect = rect()

    def AddColor(self, color=[255, 255, 255]):
        assert(self.rectData.shape[2] == 3)
        for i in range(3):
            self.rectData[:, :, i] = color[i]
        return self.rectData

    def SetValue(self, value):
        for i in range(self.rectData.shape[2]):
            self.rectData[:, :, i] = value
        return self.rectData

    def AddRectArray(self, rectArray, check=True):
        if(check):
            self.AddRectArray_v1(rectArray)
        else:
            self.AddRectArray_v2(rectArray)

    def AddRectArray_v1(self, rectArray):
        assert (isinstance(rectArray, RectArray))
        assert (rectArray.rect < self.rect)
        assert (rectArray.rect.rectPosPoint >= Point([0, 0]))
        assert (rectArray.rect.DiaCorner() <= Point(self.rect.shape()))
        assert (rectArray.rectData.shape[2] == self.rectData.shape[2])
        x1 = rectArray.rect.rectPosPoint.x
        y1 = rectArray.rect.rectPosPoint.y
        x2 = rectArray.rect.DiaCorner().x
        y2 = rectArray.rect.DiaCorner().y
        self.rectData[x1:x2, y1:y2] = rectArray.rectData
        return self.rectData

    def AddRectArray_v2(self, rectArray):
        assert (isinstance(rectArray, RectArray))
        assert (rectArray.rectData.shape[2] == self.rectData.shape[2])
        x1 = rectArray.rect.rectPosPoint.x
        y1 = rectArray.rect.rectPosPoint.y
        x2 = rectArray.rect.DiaCorner().x
        y2 = rectArray.rect.DiaCorner().y
#        ix1 = np.maximum(0, x1)
#        iy1 = np.maximum(0, y1)
#        ix2 = np.minimum(x2, self.rect.shape()[0])
#        iy2 = np.minimum(y2, self.rect.shape()[1])
#        self.rectData[ix1:ix2, iy1:iy2] = rectArray.rectData
        return self.rectData

    def __call__(self):
        return deepcopy(self)

###################################################################


class Obj(object):
    def __init__(self, data, dataMask, copy=True):
        '''
        创建对象
        '''
        assert isinstance(data, RectArray) and isinstance(dataMask, RectArray)
        assert dataMask.dtype == np.bool
        assert data.rect == dataMask.rect
        if(copy):
            data_temp = data()
            dataMask_temp = dataMask()
        else:
            data_temp = data
            dataMask_temp = dataMask
        self.rect = data_temp.rect
        self.data = data_temp.rectData
        self.dataMask = dataMask_temp.rectData
        self.rectBorder = None
        self.FindRectBorder()

    def FindRectBorder(self):
        mask = np.uint8(self.dataMask)
        rect = cv2.boundingRect(mask)
        self.rectBorder = Rect(Point(rect[0], rect[1]) +
                               self.rect.rectPosPoint,
                               (rect[2], rect[3])
                               )


###################################################################


class Trans(object):
    def __init__(self, obj):
        '''
        '''
        assert(isinstance(obj, Obj))
        self.obj_imA = obj
        self.obj_imB = None
        self.obj_flowA = None
        self.obj_flowB = None
        self.transMatrix = np.eye(3, dtype=np.float)

    def ImposeTransMatrix(self):
        pass
        # cv2.bianhuan


def GenTransMatrix(self, type_=None, trans_opts=None):
    return np.eyes(3, dtype=np.float)

###################################################################


class Board(object):
    def __init__(self, size):
        self.TransLists = []
        self.boardRect = Rect(Point(0, 0), size)
        self.imA = RectArray(self.boardRect, dtype=np.uint8)
        self.imB = RectArray(self.boardRect, dtype=np.uint8)
        self.flowA = RectArray(self.boardRect, dtype=np.float)
        self.flowB = RectArray(self.boardRect, dtype=np.float)
        # levellists

    def addTrans(self, trans):
        assert(isinstance(trans, Trans))
        self.TransLists.append(trans)

    def Gen(self):
        for trans in self.TransLists:
            test_temp = trans.obj_imA.data
            self.imA.AddRectArray(test_temp)

    def Display(self, *lists):
        # assert lists in ['imA', 'imB', 'flowA', 'flowB']
        if 'imA' in lists:
            imArray = np.uint8(self.imA.rectData)
            im = Image.fromarray(imArray)
            im.show()
        elif 'imB' in lists:
            imArray = np.uint8(self.imB.rectData)
            im = Image.fromarray(imArray)
            im.show()
        elif 'flowA' in lists:
            imArray = np.uint8(self.flowA.rectData)
            im = Image.fromarray(imArray)
            im.show()
        elif 'flowB' in lists:
            imArray = np.uint8(self.flowB.rectData)
            im = Image.fromarray(imArray)
            im.show()

###################################################################
# test
if __name__ == '__main__':
    d = Point(10, 5)
    a = Rect(Point(10, 5), [3, 4])
    b = a.Central()
    c = m.ones2([3, 4])
    print(d)
