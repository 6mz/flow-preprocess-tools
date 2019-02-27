# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
from PIL import Image
import cv2

import mynumpy as m

##################################################################
'''
本文件是一个库文件，主要用于定义下列类：
Point, Rect, RectArray, Obj, Trans, Board

它们大致的功能是：
Point: 定义图像二维坐标下的点
Rect: 定义图像二维坐标下的矩形（框）
RectArray:
    定义一组矩阵数据和其位置及大小，用于表示图像的同时存储其位置，
    包含一个Rect类和一个储存图像数据的np.array
Obj:
    定义一个对象，包含一个表明其位置和外接矩形框的Rect，以及两个储存图像数据及模板的np.array。
    简单来说，它可以储存一把椅子的位置数据（Rect），图像数据（array）及透明部分（模板）数据（array）
Trans：定义一组从ObjA到ObjB的变换，并生成相应的光流
Board:
    画布，所有Obj对象最终都会在画布上叠加呈现，画布的左上角是整个图像坐标系的原点。
    画布包含2幅变换前后的图A，B和对应的光流FlowA
'''
###################################################################


class Point(object):
    '''
    定义图像二维坐标下的点
    既可以返回(x,y)也可以返回(i,j)
    同时也支持直接相减、相加、相乘等操作
    也支持比较操作
    '''
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
        # 变成nparray
        return np.array([self.x, self.y])

    def __getitem__(self, key):
        # 定义p[0]和p[1]
        return self.y if key else self.x

    # -----------------------------------
    # 以下是加、反向加、减、反向减、数乘操作的定义
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
    # -------------------------------------------

    def __str__(self):
        return ' x:%s,y:%s ' % (self.x, self.y)

    def __repr__(self):
        return str((self.x, self.y))

    # -----------------------------------------
    # 以下定义比较操作
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
    # --------------------------------------

    def __call__(self):
        # copy
        return deepcopy(self)

###################################################################


class Rect(object):
    '''
    定义图像二维坐标下的矩形（框）
    表明矩形的位置坐标（图像坐标系下）和大小
    同时支持一些查询，如中心点、对角点、所有角点（cv2顺序）、cv2类型的矩形
    也支持比较两个矩形的大小、是否包含及重复区域
    支持移动位置
    '''
    def __init__(self, rectPos_Or_Rect, rectSize=None):
        '''
        输入：
            rectPos_Or_Rect：二维矩形左上角坐标点/另一个矩形
            rectSize：二维矩阵的大小
        变量说明：
            rectPosPoint： 左上角点
            rectSize： 矩形框大小
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
        # 返回cv2顺序的所有角点，并打包成nparray返回
        # 12
        # 34
        corners = self.AllCorners()
        pts = np.float32([corners[0].Array(),
                          corners[1].Array(),
                          corners[3].Array(),
                          corners[2].Array()
                          ])
        return pts

    def CvRect(self):
        # 返回cv2形式的矩形
        # (x,y,width,height)
        return (np.int(self.rectPosPoint[0]), np.int(self.rectPosPoint[1]),
                np.int(self.rectSize[0]), np.int(self.rectSize[1]))

    def Move(self, dis):
        # 移动矩形框的位置
        self.rectPosPoint = self.rectPosPoint + dis

    def __str__(self):
        return ' rectPosPoint:%s,rectSize:%s ' % (
                self.rectPosPoint, self.rectSize)

    def __eq__(self, other):
        # 比较两个矩形的位置大小是否都相同
        assert isinstance(other, Rect)
        return self.rectPosPoint == other.rectPosPoint and \
            (self.rectSize == other.rectSize).all()

    def __lt__(self, other):
        # 仅比较大小关系，<
        assert isinstance(other, Rect)
        return (self.rectSize[0] < other.rectSize[0] and
                self.rectSize[1] < other.rectSize[1])

    def __le__(self, other):
        # <=
        assert isinstance(other, Rect)
        return (self.rectSize[0] <= other.rectSize[0] and
                self.rectSize[1] <= other.rectSize[1])

    def __gt__(self, other):
        # >
        assert isinstance(other, Rect)
        return (self.rectSize[0] > other.rectSize[0] and
                self.rectSize[1] > other.rectSize[1])

    def __ge__(self, other):
        # >=
        assert isinstance(other, Rect)
        return (self.rectSize[0] >= other.rectSize[0] and
                self.rectSize[1] >= other.rectSize[1])

    def __and__(self, other):
        # 返回重叠部分
        assert isinstance(other, Rect)
        p1A = self.rectPosPoint
        p1B = other.rectPosPoint
        p2A = self.DiaCorner()
        p2B = other.DiaCorner()
        p1x = [p1A.x, p1B.x][p1A.x < p1B.x]
        p1y = [p1A.y, p1B.y][p1A.y < p1B.y]
        p2x = [p2A.x, p2B.x][p2A.x > p2B.x]
        p2y = [p2A.y, p2B.y][p2A.y > p2B.y]
        size = np.array([p2x-p1x, p2y-p1y])
        if ((size >= 0).all()):
            return Rect(Point(p1x, p1y), size)
        else:
            print('WARRING: Rect.__and__:\
                  The two rectangles do not coincide completely.')
            return None

    def __call__(self):
        # copy
        return deepcopy(self)

###################################################################


class RectArray(object):
    '''
    定义一组矩阵数据和其位置及大小，用于表示图像的同时存储其位置
    '''
    def __init__(self, rect, dim3=3, dtype=np.uint8):
        '''
        输入：
            rect：二维的Rect对象，表明RectArray的位置和大小。
            dim3：RectArray的第三维度大小，一般1为模板，2为光流，3为RGB图像。
            dtype：RectArray的数据类型，一般np.bool为模板，np.float为光流，
                np.uint8为RGB图像。
        数据说明：
            rectData：图像数据矩阵
            dtype：数据类型
            rect：图像矩阵的位置和大小
        '''
        assert(isinstance(rect, Rect))
        self.rectData = m.zeros3(rect.shape(), dim3, dtype)
        self.dtype = dtype
        self.rect = rect()

    def SetColor(self, color=[255, 255, 255]):
        # 图像设置为纯色
        assert(self.rectData.shape[2] == 3)
        for i in range(3):
            self.rectData[:, :, i] = color[i]
        return self.rectData

    def SetValue(self, value):
        # 图像的所有维度都设置为某个值（或某个矩阵，则要求和本身的矩阵有一样的宽高）
        for i in range(self.rectData.shape[2]):
            self.rectData[:, :, i] = value
        return self.rectData

    def AddRectArray(self, rectArray, CSYS='local', check=True):
        # 把另一个rectArray叠加到自身上，直接覆盖，不是相加
        # check为
        assert (isinstance(rectArray, RectArray))
        rect = rectArray.rect()  # 副本便于修改
        rectData = rectArray.rectData
        LF_AddRectArray(self.rect, self.rectData, rect, rectData,
                        CSYS=CSYS, check=check)

    def SetRectData(self, rectData, copy=False):
        # print(self.rectData.shape, rectData.shape)
        assert self.rectData.shape == rectData.shape
        if copy:
            rectData = rectData.copy()
        self.rectData[:] = rectData

    def __call__(self):
        return deepcopy(self)


def LF_AddRectArray(rect1, rectData1, rect2, rectData2,
                    CSYS='local', check=True, mask=None):
    # 把一个矩阵叠加到另一个矩阵上的具体实现函数，被RectArray和Obj类调用
    # 这里的叠加使用的是相对坐标，即叠加矩阵的坐标原点是被叠加矩阵的左上角点
    # 如果叠加矩阵的坐标是全局坐标，全局坐标会被变换为相对坐标参与计算
    assert CSYS in ['local', 'global']
    assert (rectData1.shape[2] == rectData2.shape[2])
    if('global' == CSYS):
        # 全局坐标转局部坐标，方便把坐标直接转化为索引
        p1 = rect1.rectPosPoint
        dis = [-p1.x, -p1.y]
        rect2.Move(dis)
    if(check):
        # check 用于判断rect1是否完全包含rect2
        LF_AddRectArray_v1(rect1, rectData1, rect2, rectData2, mask)
    else:
        LF_AddRectArray_v2(rect1, rectData1, rect2, rectData2, mask)


def LF_AddRectArray_v1(rect1, rectData1, rect2, rectData2, mask=None):
    # 严格叠加，rect1完全包含rect2才会执行
    # 这里的叠加使用的是相对坐标，即叠加矩阵的坐标原点是被叠加矩阵的左上角点
    # 因此直接与(0,0)和(shape())判断是否有包含
    assert (rect2 <= rect1)
    if ((rect2.rectPosPoint < Point([0, 0])) or
            (rect2.DiaCorner() > Point(rect1.shape()))):
        print('WARNING： LF_AddRectArray_v1: rect2 is out of range')
        return rectData1
    x1 = np.int(rect2.rectPosPoint.x + 0.5)  # 四舍五入取整
    y1 = np.int(rect2.rectPosPoint.y + 0.5)
    x2 = np.int(rect2.DiaCorner().x + 0.5)
    y2 = np.int(rect2.DiaCorner().y + 0.5)
    if mask is not None:
        assert (mask.shape[0:2] == rectData2.shape[0:2])
        rectData1[x1:x2, y1:y2][mask] = rectData2[mask]
    else:
        rectData1[x1:x2, y1:y2] = rectData2
    return rectData1


def LF_AddRectArray_v2(rect1, rectData1, rect2, rectData2, mask=None):
    # 普通的叠加，如果rect2超出rect1的范围就只保留重叠的部分
    rect2_cut = rect1 & rect2  # 计算重合部分
    if rect2_cut is None:
        # 完全不包含直接返回被叠加矩阵数据
        return rectData1
    x1 = np.int(rect2_cut.rectPosPoint.x - rect2.rectPosPoint.x + 0.5)
    y1 = np.int(rect2_cut.rectPosPoint.y - rect2.rectPosPoint.y + 0.5)
    x2 = np.int(rect2_cut.DiaCorner().x - rect2.rectPosPoint.x + 0.5)
    y2 = np.int(rect2_cut.DiaCorner().y - rect2.rectPosPoint.y + 0.5)
    rectData2_cut = rectData2[x1:x2, y1:y2]
    if mask is not None:
        mask_cut = mask[x1:x2, y1:y2]
    else:
        mask_cut = None
    return LF_AddRectArray_v1(  # 把重合部分输入
            rect1, rectData1, rect2_cut, rectData2_cut, mask_cut)

###################################################################


class Obj(object):
    '''
    最基本对象
    '''
    def __init__(self, data, dataMask, copy=True):
        '''
        输入：
            data: RectArray形式的图像数据
            dataMask: RectArray形式的图像模板数据
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
#        self.FindRectBorder()

#    def FindRectBorder(self):
#        mask = np.uint8(self.rectDataMask)
#        rect = cv2.boundingRect(mask)
#        self.rectBorder = Rect(Point(rect[0], rect[1]) +
#                               self.rect.rectPosPoint,
#                               (rect[2], rect[3])
#                               )

    def AddObj(self, obj, CSYS='global', check=False):
        # 把另一个Obj叠加在本Obj上，使用mask处理透明区域
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
        # copy
        return deepcopy(self)


###################################################################
TRANS_TYPE = ['py', 'xz', 'ts']
DEFAULT_TRANS_OPTS = {
        'py_xmin': -100,
        'py_xmax': 100,
        'py_ymin': -100,
        'py_ymax': 100,
        'xz_theta_min': 0,
        'xz_theta_max': np.pi,
        'xz_central': 'self_central'
        }


class Trans(object):
    def __init__(self, obj, same=False):
        '''
        '''
        assert(isinstance(obj, Obj))
        self.obj_imA = obj
        self.obj_imB = None
        self.obj_flowA = None
        self.obj_flowB = None
        self.Bshift = np.array([0, 0])
        self.transMatrix = np.eye(3, dtype=np.float)

    def ImposeTrans(self, pts):
        # 注意，这里的M和传统的M是转置关系，即位移变量在矩阵右侧而不是底侧
        M = cv2.getPerspectiveTransform(pts[0], pts[1])
        rectA = self.BorderRect(pts[0])
        rectB = self.BorderRect(pts[1])
        shift = rectB.rectPosPoint - rectA.rectPosPoint
        self.Bshift = shift
        M_shift = cv2.getPerspectiveTransform(pts[1], pts[1] - shift)
        assert rectA == self.obj_imA.rect
        self.TransData(M, M_shift, rectA, rectB)
        self.GenFlow(M, rectA, rectB)

    def TransData(self, M, M_shift, rectA, rectB):
        imgA = self.obj_imA.rectData
        maskA = self.obj_imA.rectDataMask
        imgB = cv2.warpPerspective(
                imgA, np.matmul(M_shift, M),  # 矩阵乘法顺序
                (rectB.rectSize[0], rectB.rectSize[1]))
        maskB = cv2.warpPerspective(
                np.uint8(maskA), np.matmul(M_shift, M),
                (rectB.rectSize[0], rectB.rectSize[1]))
        imgArrayB = RectArray(rectB)
        imgArrayB.SetRectData(imgB)
        maskArrayB = RectArray(rectB, 1, np.bool)
        maskArrayB.SetValue(maskB)
        self.obj_imB = Obj(imgArrayB, maskArrayB)
        return self.obj_imB

    def GenFlow(self, M, rectA, rectB):
        # 生成光流
        Awidth = rectA.rectSize[0]  # 宽度，列数
        Aheight = rectA.rectSize[1]
        maskA = self.obj_imA.rectDataMask
        r1 = range(0, Awidth)   # x
        r2 = range(0, Aheight)  # y
        xs, ys = np.meshgrid(r1, r2)  # 齐次坐标(x,y,z)
        zs = np.ones_like(xs)
        homoc = np.array([xs.flatten(), ys.flatten(), zs.flatten()])
        homoc = np.matmul(M, homoc)
        resx = (homoc[0, :]/homoc[2, :]).reshape(Aheight, Awidth) - xs
        resy = (homoc[1, :]/homoc[2, :]).reshape(Aheight, Awidth) - ys
        flow = np.array((resx, resy)).transpose((1, 2, 0))
        assert flow.shape == (Aheight, Awidth, 2)
        FlowArrayA = RectArray(rectA, 2, np.float)
        FlowArrayA.SetRectData(flow)
        maskArrayA = RectArray(rectA, 1, np.bool)
        maskArrayA.SetRectData(maskA)
        self.obj_flowA = Obj(FlowArrayA, maskArrayA)
        return self.obj_flowA

    def GenTrans(self, transType=None, trans_opts=DEFAULT_TRANS_OPTS):
        # ss
        assert transType in TRANS_TYPE
        Acorners = self.obj_imA.rect.CvAllCorners()
        Bcorners = Acorners
        if 'py' == transType:
            Bcorners = self.GenTrans_py(Acorners, trans_opts)
        if 'xz' == transType:
            Bcorners = self.GenTrans_xz(Acorners, trans_opts)
        return (np.float32(Acorners), np.float32(Bcorners))

    def GenTrans_py(self, Acorners, trans_opts):
        py_xmin = trans_opts['py_xmin']
        py_xmax = trans_opts['py_xmax']
        py_ymin = trans_opts['py_ymin']
        py_ymax = trans_opts['py_ymax']
        py_x = np.random.random_integers(py_xmin, py_xmax)
        py_y = np.random.random_integers(py_ymin, py_ymax)
        Bcorners = Acorners + np.array([py_x, py_y])
        return Bcorners

    def GenTrans_xz(self, Acorners, trans_opts):
        xz_theta_min = trans_opts['xz_theta_min']
        xz_theta_max = trans_opts['xz_theta_max']
        xz_central = trans_opts['xz_central']
        if xz_central == 'self_central':
            xz_point = self.BorderRect(Acorners).Central()
        else:
            xz_point = Point(0, 0)
        # 逆时针旋转的角度
        xz_theta = xz_theta_min + \
            np.random.random() * (xz_theta_max - xz_theta_min)
        xz_theta = 90 / 180 * np.pi  # !!!!!!!!!!!!!!!!!
        cos = np.cos(-xz_theta)
        sin = np.sin(-xz_theta)
        cx = xz_point.x
        cy = xz_point.y
        M = np.array([
                    [cos, -sin, (1-cos)*cx+sin*cy],
                    [sin, cos, (1-cos)*cy-sin*cx],
                    [0, 0, 1]])
        xs = Acorners[:, 0]
        ys = Acorners[:, 1]
        zs = np.ones_like(xs)
        homoc = np.array([xs, ys, zs])
        homoc = np.matmul(M, homoc)
        resx = (homoc[0, :]/homoc[2, :])
        resy = (homoc[1, :]/homoc[2, :])
        Bcorners = np.array([resx, resy]).transpose()
        print(Acorners,Bcorners)
        return Bcorners

    def BorderRect(self, pts):
        # 找到4个点的外框矩阵
        assert len(pts) == 4
        minx = 999999
        maxx = -999999
        miny = 999999
        maxy = -999999
        for pt in pts:
            x = pt[0]
            y = pt[1]
            minx = [minx, x][x < minx]
            maxx = [maxx, x][x > maxx]
            miny = [miny, y][y < miny]
            maxy = [maxy, y][y > maxy]
        size = np.array([maxx-minx, maxy-miny])
        return Rect(Point(minx, miny), size)

###################################################################


class Board(object):
    def __init__(self, size):
        self.TransLists = []
        self.boardRect = Rect(Point(0, 0), size)
        background = RectArray(self.boardRect, dtype=np.uint8)
        backgroundFlow = RectArray(self.boardRect, 2, dtype=np.float)
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
            self.imA.AddObj(trans.obj_imA)
            self.imB.AddObj(trans.obj_imB)
            self.flowA.AddObj(trans.obj_flowA)

    def Display(self, *lists):
        # assert lists in ['imA', 'imB', 'flowA', 'flowB']
        if 'imA' in lists:
            imArray = np.uint8(self.imA.rectData)
            im = Image.fromarray(imArray)
            im.save('../data/ds_v1/tmp1.jpg')
        elif 'imB' in lists:
            imArray = np.uint8(self.imB.rectData)
            im = Image.fromarray(imArray)
            im.save('../data/ds_v1/tmp2.jpg')
        elif 'flowA' in lists:
            flow_g = np.linalg.norm((self.flowA.rectData), axis=2)
            imArray = np.uint8(flow_g/(np.max(flow_g)+1)*255)
            im = Image.fromarray(imArray)
            im.save('../data/ds_v1/tmp_flow.jpg')
            flow_write('../data/ds_v1/tmp_flow.flo',self.flowA.rectData)
            return imArray
        elif 'flowB' in lists:
            imArray = np.uint8(self.flowB.rectData)
            im = Image.fromarray(imArray)
            im.show()
###################################################################


def flow_write(filename, uv, v=None):
    """ Write optical flow to file.
    If v is None, uv is assumed to contain both u and v channels,
    stacked in depth.
    Original code by Deqing Sun, adapted from Daniel Scharstein.
    """
    nBands = 2

    if v is None:
        assert(uv.ndim == 3)
        assert(uv.shape[2] == 2)
        u = uv[:, :, 0]
        v = uv[:, :, 1]
    else:
        u = uv

    assert(u.shape == v.shape)
    height, width = u.shape
    f = open(filename, 'wb')
    TAG_CHAR = b'PIEH'
    f.write(TAG_CHAR)
    np.array(width).astype(np.int32).tofile(f)
    np.array(height).astype(np.int32).tofile(f)
    # arrange into matrix form
    tmp = np.zeros((height, width*nBands))
    tmp[:, np.arange(width)*2] = u
    tmp[:, np.arange(width)*2 + 1] = v
    tmp.astype(np.float32).tofile(f)
    f.close()
###################################################################


# test
if __name__ == '__main__':
    d = Point(10, 5)
    a = Rect(Point(10, 5), [3, 4])
    b = a.Central()
    c = m.ones2([3, 4])
    print(d)
