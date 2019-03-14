# -*- coding: utf-8 -*-
from datasets_lib1 import Point
from datasets_func import FindMinAndMax
import numpy as np


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