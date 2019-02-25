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

    def Array(self):
        return np.array([self.x, self.y])

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
        if(isinstance(other, Point)):
            return np.array([x, y])
        else:
            return Point(x, y)

    def __rsub__(self, other):
        x = other[0] - self.x
        y = other[1] - self.y
        if(isinstance(other, Point)):
            return np.array([x, y])
        else:
            return Point(x, y)

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
            assert(len(rectSize) == 2 and rectSize[0] >= 0 and rectSize[1] >= 0)
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
        corner3 = self.DiaCorner()
        corner4 = corner1 + (0, self.rectSize[1])
        return (corner1, corner2, corner3, corner4)

    def CvAllCorners(self):
        corners = self.AllCorners()
        pts = np.float32([corners[0].Array(),
                          corners[1].Array(),
                          corners[3].Array(),
                          corners[2].Array()
                          ])
        return pts

    def CvRect(self):
        return (np.int(self.rectPosPoint[0]), np.int(self.rectPosPoint[1]),
                np.int(self.rectSize[0]), np.int(self.rectSize[1]))

    def Move(self, dis):
        self.rectPosPoint = self.rectPosPoint + dis

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

    def AddRectArray(self, rectArray, CSYS='local', check=True):
        assert (isinstance(rectArray, RectArray))
        rect = rectArray.rect()  # 副本便于修改
        rectData = rectArray.rectData
        LF_AddRectArray(self.rect, self.rectData, rect, rectData,
                            CSYS=CSYS, check=check)

    def __AddRectArray_v2(self, rect, rectData):
        x1 = rect.rectPosPoint.x
        y1 = rect.rectPosPoint.y
        x2 = rect.DiaCorner().x
        y2 = rect.DiaCorner().y
#        ix1 = np.maximum(0, x1)
#        iy1 = np.maximum(0, y1)
#        ix2 = np.minimum(x2, self.rect.shape()[0])
#        iy2 = np.minimum(y2, self.rect.shape()[1])
#        self.rectData[ix1:ix2, iy1:iy2] = rectArray.rectData
        return self.rectData

    def __call__(self):
        return deepcopy(self)


def LF_AddRectArray(rect1, rectData1, rect2, rectData2,
                    CSYS='local', check=True, mask=None):
    # 这里的叠加使用的是相对坐标，即叠加矩阵的坐标原点是被叠加矩阵的左上角点
    # 如果叠加矩阵的坐标是全局坐标，全局坐标会被变换为相对坐标参与计算
    assert CSYS in ['local', 'global']
    assert (rectData1.shape[2] == rectData2.shape[2])
    if('global' == CSYS):
        p1 = rect1.rectPosPoint
        dis = [-p1.x, -p1.y]
        rect2.Move(dis)
    if(check):
        LF_AddRectArray_v1(rect1, rectData1, rect2, rectData2, mask)
    else:
        pass


def LF_AddRectArray_v1(rect1, rectData1, rect2, rectData2, mask=None):
    assert (rect2 <= rect1)
    if ((rect2.rectPosPoint < Point([0, 0])) or
            (rect2.DiaCorner() > Point(rect1.shape()))):
        print('WARNING： LF_AddRectArray_v1: rect2 is out of range')
        return rectData1
    x1 = rect2.rectPosPoint.x
    y1 = rect2.rectPosPoint.y
    x2 = rect2.DiaCorner().x
    y2 = rect2.DiaCorner().y
    if mask is not None:
        assert (mask.shape[0:2] == rectData2.shape[0:2])
        rectData1[x1:x2, y1:y2][mask] = rectData2[mask]
    else:
        rectData1[x1:x2, y1:y2] = rectData2
    return rectData1
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
        self.rectData = data_temp.rectData
        self.rectDataMask = dataMask_temp.rectData
        self.rectBorder = None
        self.FindRectBorder()

    def FindRectBorder(self):
        mask = np.uint8(self.rectDataMask)
        rect = cv2.boundingRect(mask)
        self.rectBorder = Rect(Point(rect[0], rect[1]) +
                               self.rect.rectPosPoint,
                               (rect[2], rect[3])
                               )

    def AddObj(self, obj, CSYS='local', check=True):
        assert CSYS in ['local', 'global']
        assert (isinstance(obj, Obj))
        LF_AddRectArray(self.rect, self.rectData, obj.rect, obj.rectData,
                        CSYS=CSYS, check=check, mask=obj.Mask())

    def Mask(self):
        # 把1个通道的mask复制成N个通道的mask
        mask = self.rectDataMask
        shape = self.rectData.shape
        mask = mask.repeat(shape[2])
        mask = mask.reshape(shape)
        return mask


    def __call__(self):
        return deepcopy(self)


###################################################################
transTypes = ['py', 'xz', 'ts']
DEFAULT_TRANS_OPTS = {
        'py_xmin': 0,
        'py_xmax': 100,
        'py_ymin': 0,
        'py_ymax': 100,
        }


class Trans(object):
    def __init__(self, obj, same=False):
        '''
        '''
        assert(isinstance(obj, Obj))
        self.obj_imA = obj
        self.obj_imB = None
        self.obj_imB_shift = np.array([0, 0])
        self.obj_flowA = None
        self.obj_flowB = None
        self.transMatrix = np.eye(3, dtype=np.float)

    def ImposeTrans(self, pts):
        # 临时输入pair
        M = cv2.getPerspectiveTransform(pts[0], pts[1])
        print(M)
        rectA = self.obj_imA.rect
        rectB = rectA()
        imgA = self.obj_imA.rectData
        maskA = self.obj_imA.rectDataMask
        Bshift = self.Check(pts[1][0])
        rectB.Move(Bshift)
        self.obj_imB_shift = Bshift
        print(rectB,rectA)
        # 需要对矩阵大小进行修正
        # 需要判断矩阵大小
        
        #dst = cv2.warpPerspective( img, M, (width, height))
        pass
        # cv2.bianhuan

    def GenTrans(self, transType=None, trans_opts=DEFAULT_TRANS_OPTS):
        # 抽象input：平移，旋转，其他（随机）
        # 抽象out：4点对
        # input：4点，4点
        # output：M
        assert transType in transTypes
        Acorners = self.obj_imA.rect.CvAllCorners()
        Bcorners = Acorners
        if 'py' in transType:
            py_xmin = trans_opts['py_xmin']
            py_xmax = trans_opts['py_xmax']
            py_ymin = trans_opts['py_ymin']
            py_ymax = trans_opts['py_ymax']
            py_x = np.random.random_integers(py_xmin, py_xmax)
            py_y = np.random.random_integers(py_ymin, py_ymax)
            #Bcorners = Bcorners + np.array([py_x, py_y])
            # 需要改回远洋
            Bcorners = Bcorners + np.array([-10, -20])
        return (np.float32(Acorners), np.float32(Bcorners))

    def Check(self, Bpt):
        ### 需要改成对4个点判断
        Apt = self.obj_imA.rect.rectPosPoint
        dx = Bpt[0]-Apt[0]
        dx = [dx, 0][dx > 0] # 负的保留，正的为0
        dy = Bpt[1]-Apt[1]
        dy = [dy, 0][dy > 0]
        return np.array([dx, dy])
###################################################################


class Board(object):
    def __init__(self, size):
        self.TransLists = []
        self.boardRect = Rect(Point(0, 0), size)
        background = RectArray(self.boardRect, dtype=np.uint8)
        backgroundFlow = RectArray(self.boardRect, dtype=np.float)
        backgroundMask = RectArray(self.boardRect, 1, dtype=np.bool)
        self.imA = Obj(background, backgroundMask)
        self.imB = Obj(background, backgroundMask)
        self.flowA = Obj(backgroundFlow, backgroundMask)
        self.flowB = Obj(backgroundFlow, backgroundMask)
        # levellists

    def addTrans(self, trans):
        assert(isinstance(trans, Trans))
        self.TransLists.append(trans)

    def Gen(self):
        for trans in self.TransLists:
            test_temp = trans.obj_imA
            self.imA.AddObj(test_temp)

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
