# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import mynumpy as m
from datasets_lib1 import Point


# ====================== 随机函数 ========================
def FindMinAndMax(in1, in2):
    # 返回的元组小数在前大数在后
    if(in1 > in2):
        return (in2, in1)
    else:
        return (in1, in2)


def RandomSize(minSize, maxSize):
    '''
    返回一个size矩阵(1*2)
    输入：
        minSize: 格式：(x,y)，表示最小的x和y
        maxSize: 格式：(x,y)，表示最大的x和y
    '''
    assert(len(maxSize) == len(minSize) == 2)
    (minx, maxx) = FindMinAndMax(maxSize[0], minSize[0])
    (miny, maxy) = FindMinAndMax(maxSize[1], minSize[1])
    assert((maxx >= minx >= 0)and(maxy >= miny >= 0))
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return np.array([x, y])


def RandomPoint(minPoint, maxPoint):
    '''
    返回一个Point
    输入：
        minPoint: 格式：Point或(x,y)，表示点的最小x和y
        maxPoint: 格式：Point或(x,y)，表示点的最大x和y
    '''
    assert(isinstance(minPoint, Point) or len(minPoint) == 2)
    assert(isinstance(maxPoint, Point) or len(maxPoint) == 2)
    (minx, maxx) = FindMinAndMax(minPoint[0], maxPoint[0])
    (miny, maxy) = FindMinAndMax(minPoint[1], maxPoint[1])
    assert((maxx >= minx)and(maxy >= miny))
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return Point(x, y)


def RandomDis(minDis, maxDis):
    '''
    返回一个dis矩阵(1*2)
    输入：
        minDis: 格式：(x,y)，表示最小的x和y
        maxDis: 格式：(x,y)，表示最大的x和y
    '''
    if(isinstance(minDis, (int, float))):
        minx = miny = minDis
    if(isinstance(maxDis, (int, float))):
        maxx = maxy = maxDis
    (minx, maxx) = FindMinAndMax(maxDis[0], minDis[0])
    (miny, maxy) = FindMinAndMax(maxDis[1], minDis[1])
    assert (maxx >= minx) and (maxy >= miny)
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return np.array([x, y])


def NormalDis(meanDis, sigmaDis):
    if(isinstance(meanDis, (int, float))):
        meanx = meany = meanDis
    if(isinstance(sigmaDis, (int, float))):
        sigmax = sigmay = sigmaDis
    x = np.rint(np.random.normal(meanx, sigmax, 1)[0])
    y = np.rint(np.random.normal(meany, sigmay, 1)[0])
    return np.array([x, y], dtype=np.int)


def RandomAngle(minAngle, maxAngle=None, unit='r'):
    '''
    返回一个弧度为单位的角度
    输入：
        minDis: 格式：(x,y)，表示最小的x和y
        maxDis: 格式：(x,y)，表示最大的x和y
    '''
    if maxAngle is None and minAngle > 0:
        maxAngle = minAngle
        minAngle = 0
    if unit == 'd' or unit == 'degree':
        maxAngle = maxAngle / 180 * np.pi
        minAngle = minAngle / 180 * np.pi
    angle = minAngle + \
        np.random.random() * (maxAngle - minAngle)
    return angle


def NormalAngle(mean=0, sigma=1, unit='r'):
    if unit == 'd' or unit == 'degree':
        mean = mean / 180 * np.pi
        sigma = sigma / 180 * np.pi
    return np.random.normal(mean, sigma, 1)[0]


# ==================== txt文件读写 ===========================
def SaveList(fname, listname):
    with open(fname, 'w') as f:
        for line in listname:
            f.write(str(line)+'\n')


def ReadList(fname):
    with open(fname, 'r') as f:
        lists = [line.strip()
                 for line in f.readlines() if len(line.strip()) > 0]
    return lists
