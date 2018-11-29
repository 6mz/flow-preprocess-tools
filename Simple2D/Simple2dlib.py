# -*- coding: utf-8 -*-
import os.path
import numpy as np
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

sys.path.append("../Server_EasyTest")
from myflowlib import viz_flow,flow_write,flow_read,viz_flow_fromfile
from Point import point

#def draw_rect_and_save(ids,root=''):
#    backsize = np.array([640 ,480])#(x,y)
#    rectsize_min =  np.array([50,50])#(x,y)
#    rectsize_max =  np.array([200,200])#(x,y)
#
#    backarray = background_c(backsize)
#    rectsize = randrectsize(rectsize_min,rectsize_max)
#    pos1 = randpos(backsize,rectsize)
#    pos2 = randpos(backsize,rectsize)
#    while(pos1 == pos2):
#        pos2 = randpos(backsize,rectsize)
#    move = pos2 - pos1
#    pos1_n = pos1 + rectsize
#    pos2_n = pos2 + rectsize
#
#    image = Image.fromarray(backarray)
#    draw = ImageDraw.Draw(image)
#    draw.rectangle((pos1.x, pos1.y, pos1_n.x, pos1_n.y), 'red', 'red')
#    image.save(os.path.join(root,'A',str(ids)+'A.jpg'))
#
#    image = Image.fromarray(backarray)
#    draw = ImageDraw.Draw(image)
#    draw.rectangle((pos2.x, pos2.y, pos2_n.x, pos2_n.y), 'red', 'red')
#    image.save(os.path.join(root,'B',str(ids)+'B.jpg'))
#
#    gtflow = np.zeros((backsize[1],backsize[0],2),dtype='float')
#    gtflow[pos1.i:pos1_n.i, pos1.j:pos1_n.j, 0] = move[0]
#    gtflow[pos1.i:pos1_n.i, pos1.j:pos1_n.j, 1] = move[1]
#    flow_write(os.path.join(root,'gt',str(ids)+'gt.flo'),gtflow)
##    image = Image.fromarray(viz_flow(gtflow))
##    image.save(os.path.join(root,'gt_viz',str(ids)+'gt.jpg'))
#
##    print(move)
##    flow = flow_read(os.path.join(root,'gt',str(ids)+'gt.flow'))
##    image = Image.fromarray(viz_flow_fromfile(flow))
##    image.save(os.path.join(root,'gt_viz',str(ids)+'gt_fromfile.jpg'))
##    return flow
#
#def randrectsize(minsize,maxsize):
#    assert True == (minsize < maxsize).all()
#    return np.array([random.randint(minsize[0],maxsize[0]),random.randint(minsize[1],maxsize[1])])
#

#
#def background_c(backsize):
#    # x,y -> i,j
#    array = np.zeros((backsize[1], backsize[0], 3), np.uint8)
#    color = np.linspace(0,255,backsize[0])
#    color = np.vstack((color for _ in range(backsize[1])))
#    array[:, :, 0] = color
#    array[:, :, 1] = color
#    array[:, :, 2] = color
#    return array
#
def Rect1(rectSize,dtype =  np.uint8):
    # x,y -> i,j
    array = np.zeros((rectSize[1], rectSize[0]),dtype)
    return array

def Rect2(rectSize,dtype =  np.uint8):
    # x,y -> i,j
    array = np.zeros((rectSize[1], rectSize[0], 2),dtype)
    return array

def Rect2f(rectSize,dtype =  np.float):
    # x,y -> i,j
    array = np.zeros((rectSize[1], rectSize[0], 2),dtype)
    return array

def Rect3(rectSize, color = [255,255,0], dtype =  np.uint8):
    # x,y -> i,j
    array = np.zeros((rectSize[1], rectSize[0], 3), dtype)
    array[:, :, 0] = color[0]
    array[:, :, 1] = color[1]
    array[:, :, 2] = color[2]
    return array

def ij2xy(ij):
    return np.array([ij[1],ij[0]],dtype=np.int)

def xy2ij(xy):
    return np.array([xy[1],xy[0]],dtype=np.int)

def arr(lists):
    return np.array(lists)

def arri(lists):
    return np.array(lists,dtype=np.int)

def arrf(lists):
    return np.array(lists,dtype=np.float)

def ImposeRect(backgroundArray,rectArray,posPoint):
    newArray = backgroundArray.copy()
    assert len(backgroundArray.shape) == len(rectArray.shape)
    posPoint_dia = posPoint + ij2xy(rectArray.shape)
    backGroundShape = backgroundArray.shape[0:2]
    maxi = backGroundShape[0]
    maxj = backGroundShape[1]
    mini = 0
    minj = 0
    #[1,2][True] -> 2
    pos_i = [mini , posPoint.i][mini <= posPoint.i]
    pos_i = [maxi , posPoint.i][maxi >  posPoint.i]
    pos_j = [minj , posPoint.j][minj <= posPoint.j]
    pos_j = [maxj , posPoint.j][maxj >  posPoint.j]
    posDia_i = [mini , posPoint_dia.i][mini <= posPoint_dia.i]
    posDia_i = [maxi , posPoint_dia.i][maxi >  posPoint_dia.i]
    posDia_j = [minj , posPoint_dia.j][minj <= posPoint_dia.j]
    posDia_j = [maxj , posPoint_dia.j][maxj >  posPoint_dia.j]
    if len(backgroundArray.shape) == 2:
        backgroundArray[pos_i:posDia_i, pos_j:posDia_j] = rectArray
    else:
        for ii in range(backgroundArray.shape[2]):
            newArray[posPoint.i:posPoint_dia.i, posPoint.j:posPoint_dia.j, ii] = rectArray[:,:,ii]
    return newArray

def RandPos(rangePoint1,rangePoint2):
    assert type(rangePoint1) == type(rangePoint2) 
    maxx = np.max([rangePoint1.x,rangePoint2.x])
    minx = np.min([rangePoint1.x,rangePoint2.x])
    maxy = np.max([rangePoint1.y,rangePoint2.y])
    miny = np.min([rangePoint1.y,rangePoint2.y])
    return point(random.randint(minx,maxx),random.randint(miny,maxy))

def RandSize(range1,range2):
    maxx = np.max([range1[0],range2[0]])
    minx = np.min([range1[0],range2[0]])
    maxy = np.max([range1[1],range2[1]])
    miny = np.min([range1[1],range2[1]])
    return arr([random.randint(minx,maxx),random.randint(miny,maxy)])


def RandMov(posA,minMovDis,maxMovDis,rangePoint1,rangePoint2):
    minmx = minMovDis[0]
    maxmx = maxMovDis[0]
    minmy = minMovDis[1]
    maxmy = maxMovDis[1]
    maxx = np.max([rangePoint1.x,rangePoint2.x])
    minx = np.min([rangePoint1.x,rangePoint2.x])
    maxy = np.max([rangePoint1.y,rangePoint2.y])
    miny = np.min([rangePoint1.y,rangePoint2.y])
    Ax = posA.x
    Ay = posA.y
    while(1):
        mx= random.randint(minmx,maxmx)
        my= random.randint(minmy,maxmy)
        signx = random.randint(0,1)*2-1
        signy = random.randint(0,1)*2-1
        movex = signx * mx
        movey = signy * my
        Bx = Ax + movex
        By = Ay + movey
        if(minx<Bx<maxx and miny<By<maxy):break
    return point(Bx,By),arr([movex,movey])


class RectDatasets(object):
    def __init__(self,backGroundSize,backGroundColor = [255,255,255]):
        self.backGroundSize = backGroundSize
        self.backGroundColor = backGroundColor
        self.imA_Array = Rect3(backGroundSize,backGroundColor)
        self.imB_Array = Rect3(backGroundSize,backGroundColor)
        self.gtFlowArray = Rect2f(backGroundSize)
        self.setMovDis(arr([0,0]),arr([50,50]))
        self.setRectSize(arr([20,20]),arr([200,200]))
        self.setRangeMode(0)

    def setMovDis(self,minMovDis,maxMovDis):
        self.minMovDis = minMovDis
        self.maxMovDis = maxMovDis

    def setRectSize(self,minRectSize,maxRectSize):
        self.minRectSize = minRectSize
        self.maxRectSize = maxRectSize

    def setRangeMode(self,rangeMode=0):
        self.rangeMode=rangeMode

    def _setRangePoints(self):
        if(0==self.rangeMode):
            self.rangePointA1 = point(1,1)
            self.rangePointA2 = point(self.backGroundSize-self.rectSize-1)
        else:
            self.rangePointA1 = point(-self.rectSize)
            self.rangePointA2 = point(self.backGroundSize)

    def _AddRect(self):
        posA = RandPos(self.rangePointA1,self.rangePointA2)
        posB,movDis = RandMov(posA,self.minMovDis,self.maxMovDis,self.rangePointA1,self.rangePointA2)
        rectArray = Rect3(self.rectSize,[0,255,255])
        movArray = Rect2f(self.rectSize)
        movArray[:,:,:] = movDis
        self.imA_Array = ImposeRect(self.imA_Array,rectArray,posA)
        self.imB_Array = ImposeRect(self.imB_Array,rectArray,posB)
        self.gtFlowArray = ImposeRect(self.gtFlowArray,movArray,posA)
    
    def _setRandRectSize(self):
        self.rectSize = RandSize(self.minRectSize,self.maxRectSize)

    def AddRect(self,times=1):
        for _ in range(times):
            self._setRandRectSize()
            self._setRangePoints()
            self._AddRect()

backGroundSize = arr([640 ,480])#(x,y)
datasetGenerator = RectDatasets(backGroundSize)
datasetGenerator.setMovDis(arr([100,100]),arr([200,200]))
datasetGenerator.AddRect(3)

imA = Image.fromarray(datasetGenerator.imA_Array)
imB = Image.fromarray(datasetGenerator.imB_Array)
imA.show()
imB.show()