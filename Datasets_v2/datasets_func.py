# -*- coding: utf-8 -*-
"""

"""
import numpy as np


# ====================== 随机函数 ========================
def FindMinAndMax(in1, in2):
    # 返回的元组小数在前大数在后
    if(in1 > in2):
        return (in2, in1)
    else:
        return (in1, in2)


def RandomScale(minScale, maxScale):
    '''
    返回一个scale矩阵(1*2)
    输入：
        minScale: 格式：(x,y)，表示最小的x和y缩放倍数
        maxScale: 格式：(x,y)，表示最大的x和y缩放倍数
    '''
    assert(len(minScale) == len(maxScale) == 2)
    (minx, maxx) = FindMinAndMax(minScale[0], minScale[0])
    (miny, maxy) = FindMinAndMax(minScale[1], minScale[1])
    assert((maxx >= minx >= 0)and(maxy >= miny >= 0))
    x = np.random.uniform(minx, maxx)
    y = np.random.uniform(miny, maxy)
    return np.array([x, y])


def NormalScale(meanScale, sigmaScale):
    scale = np.random.normal(meanScale, sigmaScale, 1)[0]
    return scale


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
    angle = np.random.normal(minAngle, maxAngle)
    return angle


def NormalAngle(mean=0, sigma=1, unit='r'):
    if unit == 'd' or unit == 'degree':
        mean = mean / 180 * np.pi
        sigma = sigma / 180 * np.pi
    return np.random.normal(mean, sigma, 1)[0]


def RandomLevel(levelDict):
    lvN = list(levelDict.keys())
    lvP = np.array(list(levelDict.values()))
    lvP = lvP / np.sum(lvP)
    return np.random.choice(lvN, p=lvP)

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
