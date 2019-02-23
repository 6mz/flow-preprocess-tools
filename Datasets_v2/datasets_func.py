# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import mynumpy as m
from datasets_lib1 import Point


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
    assert((maxx >= minx >= 0)and(maxy >= miny >= 0))
    x = np.random.random_integers(minx, maxx)
    y = np.random.random_integers(miny, maxy)
    return Point(x, y)

