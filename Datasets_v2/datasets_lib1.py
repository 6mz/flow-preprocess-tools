# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
import mynumpy as m


###################################################################
class Point(object):
    def __init__(self,x,y=None):
        if(isinstance(x,Point)):
            self.x = x.x
            self.y = x.y
            self.i = x.i
            self.j = x.j
        elif(None == y):
            self.x = x[0]
            self.y = x[1]
            self.i = x[1]
            self.j = x[0]
        else:
            self.x = x
            self.y = y
            self.i = y
            self.j = x
    def __getitem__(self,key):#p[0] or p[1]
        return self.y if key else self.x
    def __add__(self, other):
        x = self.x+other[0]
        y = self.y+other[1]
        return Point(x,y)
    def __radd__(self, other):
        x = other[0] + self.x
        y = other[1] + self.y
        return Point(x,y)
    def __sub__(self,other):
        x = self.x-other[0]
        y = self.y-other[1]
        return np.array([x,y])
    def __rsub__(self, other):
        x = other[0] - self.x
        y = other[1] - self.y
        return np.array([x,y])
    def __mul__(self, num):
        x = self.x * num
        y = self.y * num
        return Point(x,y)
    def __str__(self):
        return ' x:%s,y:%s '%(self.x,self.y)
    def __repr__(self):
        return str((self.x,self.y))
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y
    def __lt__(self,other):
        return self.x < other.x and self.y < other.y
    def __gt__(self,other):
        return self.x > other.x and self.y > other.y
    def __call__(self):
        return deepcopy(self)

###################################################################

class Rect(object):
    '''
    
    '''
    def __init__(self,rectPos_Or_Rect,rectSize=None):
        '''
        输入：
            rectPos_Or_Rect：矩形左上角坐标点/另一个矩形
            rectSize：矩阵的大小(2维)
        '''
        if(isinstance(rectPos_Or_Rect,Point)):
            self.rectPosPoint = rectPos_Or_Rect
            assert(len(rectSize)==2 and rectSize[0]>0 and rectSize[1]>0)
            self.rectSize = np.array(rectSize,dtype = np.int)
        elif(isinstance(rectPos_Or_Rect,Rect)):
            self.rectPosPoint = rectPos_Or_Rect.rectPosPoint
            self.rectSize = rectPos_Or_Rect.rectSize

    def shape(self):
        return (self.rectSize[0],self.rectSize[1])

    def central(self):
        # 中心点
        return Point(self.rectPosPoint + self.rectSize/2)

    def diaCorner(self):
        # 对角点
        return Point(self.rectPosPoint + self.rectSize)

    def allCorners(self):
        # 所有角点，顺序：
        # 12
        # 43
        corner1 = self.rectPosPoint
        corner2 = corner1 + (self.rectSize[0],0)
        corner3 = self.diaCorner()
        corner4 = corner1 + (0,self.rectSize[1])
        return (corner1,corner2,corner3,corner4)


    def __str__(self):
        return ' rectPosPoint:%s,rectSize:%s '%(
                self.rectPosPoint,self.rectSize)
    def __call__(self):
        return deepcopy(self)

    def __eq__(self,other):
        assert isinstance(other,Rect)
        return self.rectPosPoint == other.rectPosPoint and \
               (self.rectSize == other.rectSize).all()

###################################################################

class RectArray(object):
    def __init__(self,rect,dim3 = 3, dtype = np.uint8):
        '''
        '''
        assert(isinstance(rect,Rect))
        self.rectArray = m.zeros3(rect.shape(),dim3,dtype)
        self.dtype = dtype
        self.rect = rect

    def AddColor(self,color=[255,255,255]):
        assert(self.rectArray.shape[2] == 3)
        for i in range(3):
            self.rectArray[:,:,i] = color[i]
        return self.rectArray

    def SetValue(self,value):
        for i in range(self.rectArray.shape[2]):
            self.rectArray[:,:,i] = value
        return self.rectArray

###################################################################

class Obj(object):
    def __init__(self,data,dataMask):
        '''
        创建对象
        '''
        assert isinstance(data,RectArray) and isinstance(dataMask,RectArray)
        assert dataMask.dtype == np.bool
        assert data.rect == dataMask.rect
        self.rectBorder = None
        self.dataMask = dataMask
        self.data = data


###################################################################

class Trans(object):
    def __init__(self,objA):
        '''
        '''
        assert(isinstance(objA, Obj))
        self.objA = None
        self.objB = None
        self.flowA = None
        self.flowB = None
        self.flowAmask = None
        self.flowBmask = None
        self.transMatrix = np.zeros2((3,3),dtype = np.float)

    def GenTransMatrix(self,type_,trans_opts):
        pass

    def ImposeTransMatrix(self):
        pass

###################################################################


### test
if __name__ == '__main__':
    d = Point(10,5)
    a = Rect(Point(10,5),[3,4])
    b = a.central()
    c = m.ones2([3,4])
    print(d)