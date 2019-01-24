# -*- coding: utf-8 -*-
"""

"""
from Point import Point
import numpy as np
import mynumpy as m

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
            self.rectSize = np.array(rectSize,dtype = np.int)
        elif(isinstance(rectPos_Or_Rect,Rect)):
            self.rectPosPoint = rectPos_Or_Rect.rectPosPoint
            self.rectSize = rectPos_Or_Rect.rectSize

    def shape(self):
        return (self.rectSize[0],self.rectSize[1])

    def central(self):
        return Point(self.rectPosPoint + self.rectSize/2)


#class RectArray(Rect):
#    def __init__(self,rect,data=None):
#        '''
#        输入：
#            rect
#            data
#        '''
#        if(isinstance(rect,Rect)):
#            if(data is not None):
#                assert(m.shape(data) == rect.shape())
#                self.data = data
#            else:
#                self.data = None
#        super(RectArray, self).__init__(rect)


### test
if __name__ == '__mian__':
    a = Rect(Point(10,5),[3,4])
    b = a.central()
    c = m.ones([3,4])
#d = RectArray(a,data=c)


