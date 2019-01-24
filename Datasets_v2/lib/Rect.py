# -*- coding: utf-8 -*-
"""

"""
from Point import Point
import numpy as np
import mynumpy as m



class Rect(object):
    '''
    
    '''
    def __init__(self,rectPosPoint,rectSize=None):
        '''
        输入：
            rectPosPoint：矩形左上角坐标点/另一个矩形
            rectSize：矩阵的大小(2维)
        '''
        if(isinstance(rectPosPoint,Point)):
            self.rectPosPoint = rectPosPoint
            self.rectSize = np.array(rectSize,dtype = np.int)
        elif(isinstance(rectPosPoint,Rect)):
            self.rectPosPoint = rectPosPoint.rectPosPoint
            self.rectSize = rectPosPoint.rectSize

    def shape(self):
        return (self.rectSize[0],self.rectSize[1])

    def central(self):
        return Point(self.rectPosPoint + self.rectSize/2)


class RectArray(Rect):
    def __init__(self,rect,data=None):
        '''
        输入：
            rect
            data
        '''
        if(isinstance(rect,Rect)):
            if(data is not None):
                assert(m.shape(data) == rect.shape())
                self.data = data
            else:
                self.data = None
        super(RectArray, self).__init__(rect)


### test
a = Rect(Point(10,5),[3,4])
b = a.central()
c = m.ones([3,4])
d = RectArray(a,data=c)


