# -*- coding: utf-8 -*-
import os.path
import numpy as np
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

sys.path.append("../Server_EasyTest")
from myflowlib import viz_flow,flow_write,open_flo_file
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

def arr(lists,do = None):
    if(None == do):
        return np.array(lists)
    else:
        return np.array([lists,do])

def arri(lists,do = None):
    if(None == do):
        return np.array(lists,dtype=np.int)
    else:
        return np.array([lists,do],dtype=np.int)

def arrf(lists,do = None):
    if(None == do):
        return np.array(lists,dtype=np.float)
    else:
        return np.array([lists,do],dtype=np.float)

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
        for ii in range(rectArray.shape[2]):
            newArray[posPoint.i:posPoint_dia.i, posPoint.j:posPoint_dia.j, ii] = rectArray[:,:,ii]
    return newArray

def RectAddColorArray(rectArray,colorArray):
    assert(rectArray.shape[0:2] == colorArray.shape[0:2])
    return ImposeRect(rectArray,colorArray,posPoint=point(0,0))

def RectAddColor(rectArray,color):
    for i in range(rectArray.shape[2]):
        rectArray[:,:,i] = color[i]
    return rectArray

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

def RandColor():
    r = random.randint(0,255) 
    g = random.randint(0,255) 
    b = random.randint(0,255) 
    return [r,g,b]

def RandColorArray(rectSize):
    colorArray = Rect3(rectSize)
    for i in range(3):
        colorArray[:,:,i] = np.random.randint(0,256,size=xy2ij(rectSize))#np.random not include 256
    return colorArray

def RandColorArray_2(rectSize):
    # x,y -> i,j
    array = np.zeros((rectSize[1], rectSize[0], 3), np.uint8)
    channel = np.random.randint(0,2,size=3)#np.random not include 2
    channel[0] = [1,channel[0]][channel.any()]
    if random.randint(0,1):
        color = np.linspace(0,255,rectSize[0])
        color = np.vstack((color for _ in range(rectSize[1])))
    else:
        color = np.linspace(0,255,rectSize[1])
        color = np.vstack((color for _ in range(rectSize[0])))
        color = color.T
    array[:, :, 0] = color * channel[0]
    array[:, :, 1] = color * channel[1]
    array[:, :, 2] = color * channel[2]
    return array

class RectDatasets(object):
    def __init__(self,backGroundSize,backGroundColor = [255,255,255]):
        self.backGroundSize = backGroundSize
        self.backGroundColor = backGroundColor
        self.InitBackground()
        self.setMovDis(arr([0,0]),arr([50,50]))
        self.setRectSize(arr([20,20]),arr([50,50]))
        self.setRangeMode(0)
        self.setRectColorMode(0)

    def InitBackground(self):
        self.imA_Array = Rect3(self.backGroundSize,self.backGroundColor)
        self.imB_Array = Rect3(self.backGroundSize,self.backGroundColor)
        self.gtFlowArray = Rect2f(self.backGroundSize)

    def setMovDis(self,minMovDis,maxMovDis):
        self.minMovDis = minMovDis
        self.maxMovDis = maxMovDis

    def setRectSize(self,minRectSize,maxRectSize):
        self.minRectSize = minRectSize
        self.maxRectSize = maxRectSize

    def setRangeMode(self,rangeMode=0):
        self.rangeMode = rangeMode

    def setRectColorMode(self,rectColorMode=0):
        self.rectColorMode = rectColorMode
        #0:single color 1:random array

    def setSavePath(self,rootPath = './Your datasets root path'):
        self.rootPath = rootPath

    def _AddBackgroundColor(self):
        backgroundColorArray = RandColorArray_2(self.backGroundSize)
        self.imA_Array = RectAddColorArray(self.imA_Array,backgroundColorArray)
        self.imB_Array = RectAddColorArray(self.imB_Array,backgroundColorArray)

    def _GenRandRect(self):
        self.rectSize = RandSize(self.minRectSize,self.maxRectSize)
        self.rectArray = Rect3(self.rectSize)

    def _GenRangePoints(self):
        if(0==self.rangeMode):
            self.rangePointA1 = point(1,1)
            self.rangePointA2 = point(self.backGroundSize-self.rectSize-1)
        else:
            self.rangePointA1 = point(-self.rectSize)
            self.rangePointA2 = point(self.backGroundSize)

    def _AddRandColorToRect(self):
        if   0 == self.rectColorMode:
            rectColor = RandColor()
            self.rectArray = RectAddColor(self.rectArray ,rectColor)
        elif 1 == self.rectColorMode:
            rectColorArray = RandColorArray(self.rectSize)
            self.rectArray = RectAddColorArray(self.rectArray ,rectColorArray )
        elif 2 == self.rectColorMode:
            rectColor = RandColor()
            rectColorArray = RandColorArray(self.rectSize - arr(4,4))
            self.rectArray = RectAddColor(self.rectArray ,rectColor)
            self.rectArray = ImposeRect(self.rectArray ,rectColorArray, point(2,2))

    def _AddRect(self):
        posA = RandPos(self.rangePointA1,self.rangePointA2)
        posB,movDis = RandMov(posA,self.minMovDis,self.maxMovDis,self.rangePointA1,self.rangePointA2)
        movArray = Rect2f(self.rectSize)
        movArray[:,:,:] = movDis
        self.imA_Array = ImposeRect(self.imA_Array,self.rectArray,posA)
        self.imB_Array = ImposeRect(self.imB_Array,self.rectArray,posB)
        self.gtFlowArray = ImposeRect(self.gtFlowArray,movArray,posA)

    def AddRect(self,times=1):
        self._AddBackgroundColor()
        for _ in range(times):
            self._GenRandRect()
            self._GenRangePoints()
            self._AddRandColorToRect()
            self._AddRect()

    def GenImg(self):
        self.imA = Image.fromarray(self.imA_Array)
        self.imB = Image.fromarray(self.imB_Array)
        gtArray = Rect3(ij2xy(self.gtFlowArray.shape[0:2]))
        self.gt = Image.fromarray(RectAddColorArray(gtArray,self.gtFlowArray))

    def Save(self,ids,rootPath = None):
        self.GenImg()
        if(None == rootPath):rootPath=self.rootPath
        self.imA.save(os.path.join(rootPath,'A',str(ids)+'A.png'))
        self.imB.save(os.path.join(rootPath,'B',str(ids)+'B.png'))
        flow_write(os.path.join(rootPath,'gt',str(ids)+'gt.flo'),self.gtFlowArray)
        if(0):self.gt.save(os.path.join(rootPath,'gt_viz',str(ids)+'gt.jpg'))

    def OutPutDatasets(self,path,rectNum,fileNum):
        self.setSavePath(path)
        for i in range(fileNum):
            self.AddRect(rectNum)
            self.Save(i)

def show(datasetGenerator):
    imA = Image.fromarray(datasetGenerator.imA_Array)
    imB = Image.fromarray(datasetGenerator.imB_Array)
    gtFlowArray = datasetGenerator.gtFlowArray
    gtArray = Rect3(ij2xy(gtFlowArray.shape[0:2]))
    gt = Image.fromarray(RectAddColorArray(gtArray,gtFlowArray))
    imA.show()

backGroundSize = arr([640 ,480])#(x,y)
datasetGenerator = RectDatasets(backGroundSize)
datasetGenerator.setMovDis(arr([1,1]),arr([50,50]))
datasetGenerator.setRectColorMode(2)
datasetGenerator.OutPutDatasets('../data/TESTsimple2d/rect_v3',5,50)